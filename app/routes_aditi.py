# routes.py - API Endpoints for Anomalies

"""
API Endpoints for Anomaly Detection

These endpoints will be integrated with the main Flask app later.
"""

# ============================================
# API 1: Run Detection
# ============================================
"""
@main_bp.route('/api/run-detection')
@login_required
def run_detection():
    '''Run all detection rules and return results'''
    
    # Get projects from database
    projects = Project.query.all()
    
    # Run all detections
    results = run_all_detections(projects)
    
    # Save anomalies to database
    for flag in results['details']:
        anomaly = Anomaly(
            project_id=flag.get('project_id') or flag.get('project_1_id'),
            anomaly_type=flag['type'],
            severity_score=flag['severity'],
            description=f"{flag['type']} detected for project"
        )
        # Save to database...
        db.session.add(anomaly)
    
    db.session.commit()
    
    return jsonify(results)


# ============================================
# API 2: Get Flagged Projects
# ============================================
@main_bp.route('/api/flagged')
@login_required
def get_flagged():
    '''Get all flagged projects from database'''
    
    anomalies = Anomaly.query.filter_by(reviewed=False).all()
    
    result = []
    for a in anomalies:
        data = a.to_dict()
        
        # Add project details
        project = Project.query.get(a.project_id)
        if project:
            data['work_name'] = project.work_name
            data['district'] = project.district
        
        # Add related project for duplicates
        if a.anomaly_type == 'duplicate' and a.related_project_id:
            related = Project.query.get(a.related_project_id)
            if related:
                data['related_project_name'] = related.work_name
        
        result.append(data)
    
    return jsonify(result)
"""


# ============================================
# Explanation of API Endpoints
# ============================================

print("""
📡 API ENDPOINTS READY FOR INTEGRATION

1. GET /api/run-detection
   - Triggers all anomaly detection rules
   - Saves results to database
   - Returns summary counts

2. GET /api/flagged  
   - Returns all unreviewed anomalies
   - Includes project details
   - Includes related project info for duplicates

TO INTEGRATE:
1. Import run_all_detections from anomaly.py
2. Import Anomaly from models.py
3. Add these endpoints to routes.py
4. Make sure db.session is available
""")