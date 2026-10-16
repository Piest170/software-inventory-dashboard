from db import SessionLocal
from models import Software, Cve, Eol

db = SessionLocal()

print(f"Software: {db.query(Software).count()}")
print(f"CVE: {db.query(Cve).count()}")
print(f"EOL: {db.query(Eol).count()}")

for s in db.query(Software).all():
    print(f"  - {s.name} v{s.version}")

db.close()