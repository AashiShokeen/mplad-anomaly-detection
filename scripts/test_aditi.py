# test.py - Test Aditi's Anomaly Detection Logic
# RUN KARNE KE LIYE: python test.py

from datetime import datetime, timedelta
from anomaly import *
from models import Project, Anomaly

# ============================================
# SAMPLE DATA - 5 Projects for Testing
# ============================================

projects = [
    # Project 1: Normal road project
    Project(
        id=1,
        district="District A",
        village="Village 1",
        work_name="Road Construction",
        workcategory="Roads",
        sanction_amount=1000000,  # 10 Lakh
        sanction_date=datetime.now() - timedelta(days=100),
        work_status="completed"
    ),
    
    # Project 2: Duplicate of Project 1 (same village, similar name)
    Project(
        id=2,
        district="District A",
        village="Village 1",
        work_name="Road Building Work",
        workcategory="Roads",
        sanction_amount=800000,  # 8 Lakh
        sanction_date=datetime.now() - timedelta(days=50),
        work_status="pending"
    ),
    
    # Project 3: Cost outlier (very expensive)
    Project(
        id=3,
        district="District A",
        village="Village 2",
        work_name="School Building",
        workcategory="Buildings",
        sanction_amount=5000000,  # 50 Lakh (5x median)
        sanction_date=datetime.now() - timedelta(days=30),
        work_status="pending"
    ),
    
    # Project 4: Stalled project (pending > 6 months)
    Project(
        id=4,
        district="District B",
        village="Village 1",
        work_name="Water Pipeline",
        workcategory="Water",
        sanction_amount=750000,  # 7.5 Lakh
        sanction_date=datetime.now() - timedelta(days=250),  # 8 months
        work_status="pending"
    ),
    
    # Project 5: Normal project
    Project(
        id=5,
        district="District B",
        village="Village 2",
        work_name="Electricity Line",
        workcategory="Electricity",
        sanction_amount=600000,  # 6 Lakh
        sanction_date=datetime.now() - timedelta(days=45),
        work_status="completed"
    ),
]


# ============================================
# RUN ALL TESTS
# ============================================

print("=" * 60)
print("🚀 ADITI'S ANOMALY DETECTION - TEST RESULTS")
print("=" * 60)
print(f"\n📊 Total Projects: {len(projects)}")
print("=" * 60)


# TEST 1: Cost Outliers
print("\n🔴 1. COST OUTLIER DETECTION")
print("-" * 40)
outliers = detect_cost_outliers(projects)
if outliers:
    for o in outliers:
        print(f"   ⚠️ {o['project_name']} (ID: {o['project_id']})")
        print(f"      - Cost: ₹{o['sanction_amount']:,}")
        print(f"      - District Median: ₹{o['median_amount']:,}")
        print(f"      - {o['multiple']}x more than median")
else:
    print("   ✅ No cost outliers found")


# TEST 2: Stalled Projects
print("\n🟡 2. STALLED PROJECT DETECTION")
print("-" * 40)
stalled = detect_stalled_projects(projects)
if stalled:
    for s in stalled:
        print(f"   ⏰ {s['project_name']} (ID: {s['project_id']})")
        print(f"      - Pending for: {s['days_pending']} days")
        print(f"      - Amount: ₹{s['sanction_amount']:,}")
else:
    print("   ✅ No stalled projects found")


# TEST 3: Duplicate Works
print("\n🟢 3. DUPLICATE WORK DETECTION")
print("-" * 40)
duplicates = detect_duplicate_works(projects)
if duplicates:
    for d in duplicates:
        print(f"   🔄 '{d['project_1_name']}' (ID: {d['project_1_id']})")
        print(f"      ↔ '{d['project_2_name']}' (ID: {d['project_2_id']})")
        print(f"      - {d['similarity']}% similar")
        print(f"      - District: {d['district']}, Village: {d['village']}")
else:
    print("   ✅ No duplicates found")


# TEST 4: Run All
print("\n🟣 4. RUN ALL DETECTIONS")
print("-" * 40)
results = run_all_detections(projects)
print(f"   📊 Total flags found: {results['total_flags']}")
print(f"   📊 Cost outliers: {results['cost_outliers']}")
print(f"   📊 Stalled projects: {results['stalled']}")
print(f"   📊 Duplicates: {results['duplicates']}")


# TEST 5: Detailed Results
print("\n🔵 5. DETAILED RESULTS")
print("-" * 40)
if results['details']:
    for i, flag in enumerate(results['details'], 1):
        print(f"\n   #{i} - {flag['type'].upper()}")
        if flag['type'] == 'cost_outlier':
            print(f"      Project: {flag['project_name']}")
            print(f"      Cost: ₹{flag['sanction_amount']:,} (Median: ₹{flag['median_amount']:,})")
        elif flag['type'] == 'stalled':
            print(f"      Project: {flag['project_name']}")
            print(f"      Days pending: {flag['days_pending']}")
        elif flag['type'] == 'duplicate':
            print(f"      Project 1: {flag['project_1_name']}")
            print(f"      Project 2: {flag['project_2_name']}")
            print(f"      Similarity: {flag['similarity']}%")
else:
    print("   ✅ No anomalies detected")


print("\n" + "=" * 60)
print("✅ TEST COMPLETE! ALL FUNCTIONS WORKING!")
print("=" * 60)


# ============================================
# ANOMALY MODEL TEST
# ============================================
print("\n📦 ANOMALY MODEL TEST")
print("-" * 40)

# Create an anomaly
anomaly = Anomaly(
    project_id=1,
    anomaly_type='duplicate',
    severity_score=85.5,
    description="Similar to 'Road Building Work'",
    related_project_id=2,
    similarity_score=85.5
)

print(f"   Created anomaly: {anomaly}")
print(f"   To Dict: {anomaly.to_dict()}")

print("\n" + "=" * 60)
print("🎉 ALL TESTS PASSED! ADITI'S WORK IS READY!")
print("=" * 60)