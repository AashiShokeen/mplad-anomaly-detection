# app/routes.py
from flask import render_template, jsonify, request, send_file, Blueprint
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
    return render_template('dashboard.html')

@main_bp.route('/dashboard')
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