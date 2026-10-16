from db import SessionLocal
from models import Software
from sqlalchemy import or_, func
from sqlalchemy.orm import joinedload

db = SessionLocal()

print("=== ทดสอบแบบ Dashboard จริง ===\n")

# จำลองการค้นหา 'X' แบบที่ main.py ทำ
q = "X"
pattern = f"%{q}%"

query = db.query(Software).options(
    joinedload(Software.cves),
    joinedload(Software.eols),
)

query = query.filter(
    or_(
        Software.name.ilike(pattern),
        Software.vendor.ilike(pattern),
        Software.version.ilike(pattern),
        Software.category.ilike(pattern),
        Software.operating_system.ilike(pattern),
        Software.ip_address.ilike(pattern),
    )
)

results = query.order_by(Software.name).all()

print(f"ค้นหา '{q}' เจอ {len(results)} รายการ:")
for s in results:
    print(f"  - {s.name} (ID: {s.id}, Vendor: {s.vendor})")

db.close()