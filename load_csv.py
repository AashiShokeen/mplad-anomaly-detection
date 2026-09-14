# load_csv.py — Robust parser for MPLAD hybrid CSV
import re
import os
from datetime import datetime
from app import create_app, db
from app.models import Project

app = create_app()
CSV_PATH = 'data/mplad_cleaned_final.csv'


def parse_date(val):
    try:
        return datetime.strptime(str(val).strip().strip('"'), '%Y-%m-%d')
    except Exception:
        return None


def parse_amount(val):
    try:
        return float(str(val).replace(',', '').replace('"', '').strip())
    except Exception:
        return 0.0


def extract_fields(line):
    line = line.strip()
    if not line:
        return []

    # Outer quotes wrap the whole data row, closing right before ",Unknown" or ",0.0"
    if line.startswith('"'):
        m = re.search(r'",\s*(?:Unknown|0\.0)', line)
        if m:
            block = line[1:m.start()]
            parts = block.split(';""')
            return [p.strip().strip('"') for p in parts]

    # Fallback
    return [p.strip().strip('"') for p in line.split(';')]


def load():
    with app.app_context():
        Project.query.delete()
        db.session.commit()
        print("Cleared projects")

        if not os.path.exists(CSV_PATH):
            print("File not found: " + CSV_PATH)
            return

        count = 0
        skipped = 0

        with open(CSV_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            next(f)  # skip fused header

            for line in f:
                parts = extract_fields(line)
                if len(parts) < 12:
                    skipped += 1
                    continue

                try:
                    name = (parts[1] if len(parts) > 1 and parts[1] else 'Unknown Work')[:200]
                    category = (parts[2] if len(parts) > 2 and parts[2] else 'Normal/Others')[:100]
                    state = parts[3] if len(parts) > 3 else ''
                    city = parts[6] if len(parts) > 6 else ''
                    block = parts[8] if len(parts) > 8 else ''
                    village = parts[9] if len(parts) > 9 else ''
                    date_str = parts[10] if len(parts) > 10 else ''
                    amount_str = parts[11] if len(parts) > 11 else '0'
                    status = parts[12] if len(parts) > 12 else 'pending'

                    district = 'Unknown'
                    for candidate in [block, city, village, state]:
                        if candidate and candidate.strip():
                            district = candidate
                            break

                    p = Project(
                        name=name,
                        district=district[:100],
                        work_category=category[:100],
                        amount=parse_amount(amount_str),
                        village=village[:100],
                        sanction_date=parse_date(date_str),
                        work_status=status[:50],
                    )
                    db.session.add(p)
                    count += 1

                    if count % 100 == 0:
                        db.session.commit()
                except Exception:
                    skipped += 1
                    continue

        db.session.commit()
        print("DONE! Loaded " + str(count) + " projects. Skipped " + str(skipped) + ".")


if __name__ == '__main__':
    load()