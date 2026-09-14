# run_detection.py — Run detection rules and create Anomalies
from datetime import datetime
from statistics import median
from difflib import SequenceMatcher
from collections import defaultdict

from app import create_app, db
from app.models import Project, Anomaly

app = create_app()

def similarity(a, b):
    if not a or not b:
        return 0
    return int(SequenceMatcher(None, a.lower(), b.lower()).ratio() * 100)

def detect_cost_outliers():
    """Flag projects > 3x median for same work_category"""
    groups = defaultdict(list)
    for p in Project.query.all():
        if p.work_category and p.amount:
            groups[p.work_category].append(p)

    flagged = []
    for category, projects in groups.items():
        if len(projects) < 3:
            continue
        med = median([p.amount for p in projects])
        if med <= 0:
            continue
        for p in projects:
            if p.amount > med * 3:
                multiple = round(p.amount / med, 2)
                flagged.append((p, 'cost_outlier', multiple,
                    f"Cost is {multiple}x the category median (₹{med/100000:.1f}L)"))
    return flagged

def detect_stalled():
    """Flag projects pending > 180 days with amount > ₹5L"""
    today = datetime.now()
    flagged = []
    for p in Project.query.all():
        if not p.sanction_date:
            continue
        if (p.amount or 0) < 500000:
            continue
        days = (today - p.sanction_date).days
        if days > 180:
            flagged.append((p, 'stalled', days,
                f"Pending for {days} days with ₹{p.amount/100000:.1f}L allocated"))
    return flagged

def detect_duplicates():
    """Flag projects with similar names in same district"""
    projects = Project.query.all()
    groups = defaultdict(list)
    for p in projects:
        if p.district:
            groups[p.district].append(p)

    flagged = []
    seen = set()
    for district, plist in groups.items():
        if len(plist) < 2:
            continue
        for i in range(len(plist)):
            for j in range(i+1, len(plist)):
                if i in seen and j in seen:
                    continue
                sim = similarity(plist[i].name, plist[j].name)
                if sim > 75:
                    seen.add(i); seen.add(j)
                    flagged.append((plist[i], 'duplicate', sim,
                        f"Duplicate of '{plist[j].name[:50]}' ({sim}% match)"))
    return flagged

def run():
    with app.app_context():
        # Clear old anomalies
        Anomaly.query.delete()
        db.session.commit()
        print("🗑️  Cleared old anomalies")

        total = 0

        # Cost outliers
        cost = detect_cost_outliers()
        for p, typ, sev, desc in cost:
            db.session.add(Anomaly(
                project_id=p.id, anomaly_type=typ,
                severity_score=sev, description=desc
            ))
            total += 1
        print(f"💰 Cost outliers: {len(cost)}")

        # Stalled
        stalled = detect_stalled()
        for p, typ, sev, desc in stalled:
            db.session.add(Anomaly(
                project_id=p.id, anomaly_type=typ,
                severity_score=sev, description=desc
            ))
            total += 1
        print(f"⏰ Stalled projects: {len(stalled)}")

        # Duplicates
        dupes = detect_duplicates()
        for p, typ, sev, desc in dupes:
            db.session.add(Anomaly(
                project_id=p.id, anomaly_type=typ,
                severity_score=sev, description=desc
            ))
            total += 1
        print(f"📋 Duplicates: {len(dupes)}")

        db.session.commit()
        print(f"\n🎉 DONE! Created {total} anomalies.")

if __name__ == '__main__':
    run()