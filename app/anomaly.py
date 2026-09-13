# anomaly.py — Aditi + Bhoomi merged

from datetime import datetime
from difflib import SequenceMatcher
from statistics import median


def similarity_ratio(a, b):
    """Return similarity between two strings (0-100)"""
    if not a or not b:
        return 0
    return int(SequenceMatcher(None, a, b).ratio() * 100)


def detect_cost_outliers(projects):
    """Detect projects with cost > 3x district median"""
    district_stats = {}
    for p in projects:
        if p.district and p.workcategory and p.sanction_amount:
            key = (p.district, p.workcategory)
            district_stats.setdefault(key, []).append(p.sanction_amount)

    medians = {}
    for (district, category), amounts in district_stats.items():
        if len(amounts) >= 3:
            medians[(district, category)] = median(amounts)

    outliers = []
    for p in projects:
        key = (p.district, p.workcategory)
        if key in medians:
            med = medians[key]
            if med > 0 and p.sanction_amount > med * 3:
                outliers.append({
                    'project_id': p.id,
                    'project_name': p.work_name,
                    'district': p.district,
                    'sanction_amount': p.sanction_amount,
                    'median_amount': med,
                    'multiple': round(p.sanction_amount / med, 2),
                    'type': 'cost_outlier',
                    'severity': round(p.sanction_amount / med, 2)
                })
    return outliers


def detect_stalled_projects(projects):
    """Detect projects pending > 6 months with amount > ₹5L"""
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
                            'days_pending': days_pending,
                            'type': 'stalled',
                            'severity': days_pending
                        })
    return stalled


def detect_duplicate_works(projects):
    """Detect projects with similar descriptions in same district/village"""
    grouped = {}
    for p in projects:
        key = (p.district, p.village or 'Unknown')
        grouped.setdefault(key, []).append(p)

    duplicates = []
    for (district, village), projs in grouped.items():
        if len(projs) < 2:
            continue
        for i in range(len(projs)):
            for j in range(i + 1, len(projs)):
                p1, p2 = projs[i], projs[j]
                sim = similarity_ratio(p1.work_name, p2.work_name)
                if sim > 70:
                    duplicates.append({
                        'project_1_id': p1.id,
                        'project_1_name': p1.work_name,
                        'project_2_id': p2.id,
                        'project_2_name': p2.work_name,
                        'district': district,
                        'similarity': sim,
                        'type': 'duplicate',
                        'severity': sim
                    })
    return duplicates


def run_all_detections(projects):
    """Run all 3 detection rules"""
    outliers = detect_cost_outliers(projects)
    stalled = detect_stalled_projects(projects)
    duplicates = detect_duplicate_works(projects)
    return {
        'total_flags': len(outliers) + len(stalled) + len(duplicates),
        'cost_outliers': len(outliers),
        'stalled': len(stalled),
        'duplicates': len(duplicates)
    }