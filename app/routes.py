# app/routes.py
from flask import render_template, jsonify, request, send_file, Blueprint, redirect, url_for
from flask_login import login_required
from app import db
from app.models import Project, Anomaly
import io, csv

main_bp = Blueprint('main', __name__)

def safe_date(value, fmt='%Y-%m-%d'):
    if value is None:
        return None
    try:
        return value.strftime(fmt)
    except Exception:
        return str(value)

@main_bp.route('/')
def index():
    from flask_login import current_user
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/analytics')
def analytics():
    return render_template('analytics.html')

@main_bp.route('/flagged')
def flagged():
    return render_template('flagged.html')

@main_bp.route('/projects')
def projects():
    return render_template('projects.html')

@main_bp.route('/api/projects')
def api_projects():
    projects = Project.query.limit(500).all()
    return jsonify([{
        'id': p.id, 'name': p.name, 'work_category': p.work_category,
        'district': p.district, 'village': p.village, 'amount': p.amount or 0,
        'work_status': p.work_status, 'sanction_date': safe_date(p.sanction_date)
    } for p in projects])

@main_bp.route('/api/flagged')
def api_flagged():
    anomalies = Anomaly.query.order_by(Anomaly.severity_score.desc()).limit(500).all()
    result = []
    for a in anomalies:
        p = Project.query.get(a.project_id) if a.project_id else None
        result.append({
            'id': a.id,
            'project_id': a.project_id,
            'type': a.anomaly_type,
            'anomaly_type': a.anomaly_type,
            'severity': a.severity_score,
            'description': a.description,
            'detected_at': safe_date(a.detected_at, '%Y-%m-%d %H:%M'),
            'reviewed': a.reviewed,
            'notes': a.notes,
            'work_name': p.name if p else 'Unknown',
            'district': p.district if p else 'N/A',
            'sanction_amount': p.amount if p else 0,
        })
    return jsonify(result)

@main_bp.route('/api/dashboard/stats')
def api_dashboard_stats():
    total_projects = Project.query.count()
    total_anomalies = Anomaly.query.count()
    unreviewed = Anomaly.query.filter_by(reviewed=False).count()
    total_amount = db.session.query(db.func.sum(Project.amount)).scalar() or 0
    return jsonify({
        'total_projects': total_projects,
        'total_anomalies': total_anomalies,
        'unreviewed_anomalies': unreviewed,
        'total_amount_cr': round(float(total_amount) / 10000000, 2)
    })

@main_bp.route('/api/anomalies/<int:anomaly_id>/review', methods=['POST'])
def api_mark_reviewed(anomaly_id):
    a = Anomaly.query.get(anomaly_id)
    if not a:
        return jsonify({'error': 'Anomaly not found'}), 404
    a.reviewed = True
    data = request.get_json(silent=True) or {}
    a.notes = data.get('notes', 'Reviewed')
    db.session.commit()
    return jsonify({'success': True})

@main_bp.route('/api/district-comparison')
def api_district_comparison():
    projects = Project.query.all()
    data = {}
    for p in projects:
        if not p.district:
            continue
        if p.district not in data:
            data[p.district] = {
                'district': p.district,
                'state': '',
                'total_projects': 0,
                'total_amount': 0,
                'stalled': 0,
            }
        d = data[p.district]
        d['total_projects'] += 1
        d['total_amount'] += p.amount or 0
        if (p.work_status or '').lower() == 'stalled':
            d['stalled'] += 1

    for d in data.values():
        tp = d['total_projects']
        d['stalled_rate'] = round((d['stalled'] / tp) * 100, 1) if tp else 0

    result = sorted(data.values(), key=lambda x: x['stalled_rate'], reverse=True)
    return jsonify(result)

@main_bp.route('/api/dashboard/districts')
def api_districts_count():
    from sqlalchemy import func
    count = db.session.query(func.count(func.distinct(Project.district))).scalar() or 0
    return jsonify({'district_count': count})

@main_bp.route('/api/dashboard/panels')
def api_dashboard_panels():
    from sqlalchemy import func

    # 1. Status breakdown
    statuses = db.session.query(
        Project.work_status, func.count(Project.id)
    ).group_by(Project.work_status).all()
    status_map = {s or 'unknown': c for s, c in statuses}

    # 2. Top MPs by total amount (extract from project name if MP info exists)
    # We'll use district as proxy since we don't have MP field
    top_districts = db.session.query(
        Project.district, func.sum(Project.amount)
    ).filter(Project.district.isnot(None)).group_by(
        Project.district
    ).order_by(func.sum(Project.amount).desc()).limit(3).all()

    # 3. Allocation by district (top 5)
    top5 = db.session.query(
        Project.district, func.sum(Project.amount)
    ).filter(Project.district.isnot(None)).group_by(
        Project.district
    ).order_by(func.sum(Project.amount).desc()).limit(5).all()

    # 4. Recent cost outliers
    cost_anomalies = Anomaly.query.filter_by(
        anomaly_type='cost_outlier'
    ).order_by(Anomaly.severity_score.desc()).limit(3).all()

    outliers = []
    for a in cost_anomalies:
        p = Project.query.get(a.project_id)
        if p:
            outliers.append({
                'project': p.name[:60] if p.name else 'Unknown',
                'district': p.district or 'N/A',
                'amount': p.amount or 0,
                'description': a.description,
                'severity': a.severity_score,
            })

    # 5. High-priority count (severity > 5)
    high_priority = Anomaly.query.filter(Anomaly.severity_score > 5).count()

    # 6. District count
    district_count = db.session.query(
        func.count(func.distinct(Project.district))
    ).scalar() or 0

    return jsonify({
        'status_map': status_map,
        'total_projects': Project.query.count(),
        'top_districts': [{'district': d, 'amount': float(a or 0)} for d, a in top_districts],
        'top5_districts': [{'district': d, 'amount': float(a or 0)} for d, a in top5],
        'outliers': outliers,
        'high_priority': high_priority,
        'district_count': district_count,
    })