# anomaly.py - Aditi's Anomaly Detection Logic

from datetime import datetime
from fuzzywuzzy import fuzz

# ============================================
# FUNCTION 1: Cost Outlier Detection
# ============================================
def detect_cost_outliers(projects):
    """
    Detect projects with cost > 3x district median
    projects: list of Project objects
    Returns: list of outliers
    """
    
    # Calculate median per district for each work category
    district_stats = {}
    for p in projects:
        if p.district and p.workcategory and p.sanction_amount:
            key = (p.district, p.workcategory)
            if key not in district_stats:
                district_stats[key] = []
            district_stats[key].append(p.sanction_amount)
    
    medians = {}
    for (district, category), amounts in district_stats.items():
        if len(amounts) >= 3:
            sorted_amounts = sorted(amounts)
            n = len(sorted_amounts)
            median = sorted_amounts[n // 2] if n % 2 == 1 else (
                sorted_amounts[n // 2 - 1] + sorted_amounts[n // 2]
            ) / 2
            medians[(district, category)] = median
    
    outliers = []
    for p in projects:
        key = (p.district, p.workcategory)
        if key in medians:
            median = medians[key]
            if median > 0 and p.sanction_amount > median * 3:
                outliers.append({
                    'project_id': p.id,
                    'project_name': p.work_name,
                    'district': p.district,
                    'workcategory': p.workcategory,
                    'sanction_amount': p.sanction_amount,
                    'median_amount': median,
                    'multiple': round(p.sanction_amount / median, 2),
                    'type': 'cost_outlier',
                    'severity': round(p.sanction_amount / median, 2)
                })
    
    return outliers


# ============================================
# FUNCTION 2: Stalled Project Detection
# ============================================
def detect_stalled_projects(projects):
    """
    Detect projects pending > 6 months with amount > ₹5L
    """
    stalled = []
    today = datetime.now()
    
    for p in projects:
        if p.work_status and 'pending' in p.work_status.lower():
            if p.sanction_amount and p.sanction_amount > 500000:
                if p.sanction_date:
                    days_pending = (today - p.sanction_date).days
                    if days_pending > 180:
                        stalled.append({
                            'project_id': p.id,
                            'project_name': p.work_name,
                            'district': p.district,
                            'sanction_amount': p.sanction_amount,
                            'sanction_date': p.sanction_date.strftime('%Y-%m-%d'),
                            'days_pending': days_pending,
                            'type': 'stalled',
                            'severity': days_pending
                        })
    
    return stalled


# ============================================
# FUNCTION 3: Duplicate Work Detection
# ============================================
def detect_duplicate_works(projects):
    """
    Detect projects with similar descriptions in same district/village
    """
    grouped = {}
    for p in projects:
        key = (p.district, p.village or 'Unknown')
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(p)
    
    duplicates = []
    
    for (district, village), projs in grouped.items():
        if len(projs) < 2:
            continue
        
        for i in range(len(projs)):
            for j in range(i+1, len(projs)):
                p1 = projs[i]
                p2 = projs[j]
                
                similarity = fuzz.ratio(p1.work_name or '', p2.work_name or '')
                
                if similarity > 70:
                    duplicates.append({
                        'project_1_id': p1.id,
                        'project_1_name': p1.work_name,
                        'project_2_id': p2.id,
                        'project_2_name': p2.work_name,
                        'district': district,
                        'village': village,
                        'similarity': similarity,
                        'amount_1': p1.sanction_amount,
                        'amount_2': p2.sanction_amount,
                        'type': 'duplicate',
                        'severity': similarity
                    })
    
    return duplicates


# ============================================
# FUNCTION 4: Run All Detections
# ============================================
def run_all_detections(projects):
    """Run all three detection rules"""
    
    all_flags = []
    
    # 1. Cost outliers
    outliers = detect_cost_outliers(projects)
    for item in outliers:
        all_flags.append(item)
    
    # 2. Stalled projects
    stalled = detect_stalled_projects(projects)
    for item in stalled:
        all_flags.append(item)
    
    # 3. Duplicate works
    duplicates = detect_duplicate_works(projects)
    for item in duplicates:
        all_flags.append(item)
    
    return {
        'total_flags': len(all_flags),
        'cost_outliers': len(outliers),
        'stalled': len(stalled),
        'duplicates': len(duplicates),
        'details': all_flags
    }