# models.py - Anomaly Model

from datetime import datetime

class Anomaly:
    """
    Anomaly Model - Stores detected issues in projects
    
    Attributes:
    - id: Unique identifier
    - project_id: ID of the flagged project
    - anomaly_type: cost_outlier, stalled, or duplicate
    - severity_score: Float value indicating severity
    - description: Text description of the anomaly
    - detected_at: Timestamp when detected
    - reviewed: Boolean flag if reviewed by admin
    - notes: Admin notes for follow-up
    - related_project_id: For duplicate anomalies (ID of similar project)
    - similarity_score: For duplicate anomalies (similarity percentage)
    """
    
    def __init__(self, project_id=None, anomaly_type=None, severity_score=0.0, 
                 description=None, related_project_id=None, similarity_score=None):
        self.id = None
        self.project_id = project_id
        self.anomaly_type = anomaly_type  # cost_outlier, stalled, duplicate
        self.severity_score = severity_score
        self.description = description
        self.detected_at = datetime.now()
        self.reviewed = False
        self.notes = None
        self.related_project_id = related_project_id
        self.similarity_score = similarity_score
    
    def to_dict(self):
        """Convert anomaly to dictionary for API response"""
        data = {
            'id': self.id,
            'project_id': self.project_id,
            'anomaly_type': self.anomaly_type,
            'severity': self.severity_score,
            'description': self.description,
            'detected_at': self.detected_at.strftime('%Y-%m-%d %H:%M'),
            'reviewed': self.reviewed
        }
        
        if self.anomaly_type == 'duplicate':
            data['related_project_id'] = self.related_project_id
            data['similarity'] = self.similarity_score
        
        return data
    
    def __repr__(self):
        return f"<Anomaly {self.id}: {self.anomaly_type} - {self.project_id}>"


# ============================================
# Project Class (for testing without database)
# ============================================
class Project:
    """Temporary Project class for testing"""
    def __init__(self, id, district, village, work_name, workcategory, 
                 sanction_amount, sanction_date, work_status):
        self.id = id
        self.district = district
        self.village = village
        self.work_name = work_name
        self.workcategory = workcategory
        self.sanction_amount = sanction_amount
        self.sanction_date = sanction_date
        self.work_status = work_status