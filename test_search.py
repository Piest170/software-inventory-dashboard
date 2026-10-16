from db import SessionLocal
from models import Software
from sqlalchemy import or_

db = SessionLocal()

print("=== ทดสอบการค้นหาแบบ Dashboard ===\n")

# ทดสอบ 1: ค้นหา 'X' ด้วย ilike (แบบที่ Dashboard ใช้)
print("--- ค้นหา 'X' ด้วย ilike ---")
results = db.query(Software).filter(
    Software.name.ilike('%X%')
).all()
print(f"เจอ {len(results)} รายการ:")
for s in results:
    print(f"  - {s.name}")

# ทดสอบ 2: ค้นหา 'x' ด้วย ilike
print("\n--- ค้นหา 'x' ด้วย ilike ---")
results = db.query(Software).filter(
    Software.name.ilike('%x%')
).all()
print(f"เจอ {len(results)} รายการ:")
for s in results:
    print(f"  - {s.name}")

# ทดสอบ 3: ค้นหา 'X' ด้วย like ธรรมดา
print("\n--- ค้นหา 'X' ด้วย like ธรรมดา ---")
results = db.query(Software).filter(
    Software.name.like('%X%')
).all()
print(f"เจอ {len(results)} รายการ:")
for s in results:
    print(f"  - {s.name}")

# ทดสอบ 4: ค้นหา 'x' ด้วย like ธรรมดา
print("\n--- ค้นหา 'x' ด้วย like ธรรมดา ---")
results = db.query(Software).filter(
    Software.name.like('%x%')
).all()
print(f"เจอ {len(results)} รายการ:")
for s in results:
    print(f"  - {s.name}")

# ทดสอบ 5: ค้นหา 'X' ด้วย func.lower()
print("\n--- ค้นหา 'X' ด้วย func.lower() ---")
from sqlalchemy import func
results = db.query(Software).filter(
    func.lower(Software.name).like('%x%')
).all()
print(f"เจอ {len(results)} รายการ:")
for s in results:
    print(f"  - {s.name}")

# เช็คข้อมูลทั้งหมด
print("\n=== ข้อมูล Software ทั้งหมด ===")
all_software = db.query(Software).order_by(Software.name).all()
print(f"รวม {len(all_software)} รายการ:")
for s in all_software:
    print(f"  - {s.name} (ID: {s.id})")

db.close()