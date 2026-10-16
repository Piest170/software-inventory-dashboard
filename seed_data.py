from datetime import date
from db import SessionLocal
from models import Software, Cve, Eol

db = SessionLocal()

if db.query(Software).count() == 0:
    openssl = Software(
        name="OpenSSL", vendor="OpenSSL Project", version="1.1.1",
        category="Library", operating_system="Windows Server 2022",
        install_location=r"C:\OpenSSL", ip_address="192.168.1.10",
        last_scan_date=date.today(),
    )
    python_sw = Software(
        name="Python", vendor="Python Software Foundation", version="3.8.10",
        category="Runtime", operating_system="Windows Server 2019",
        install_location=r"C:\Python38", ip_address="192.168.1.20",
        last_scan_date=date.today(),
    )
    node = Software(
        name="Node.js", vendor="OpenJS Foundation", version="14.21.3",
        category="Runtime", operating_system="Windows 11",
        install_location=r"C:\Program Files\nodejs", ip_address="192.168.1.30",
        last_scan_date=date.today(),
    )
    db.add_all([openssl, python_sw, node])
    db.flush()

    db.add_all([
        Cve(software_id=openssl.id, cve_id="CVE-2023-0286", severity="HIGH",
            cvss_score=7.5, description="Use-after-free in BIO_new_NDEF",
            published_date=date(2023, 2, 8), fixed_version="1.1.1t"),
        Cve(software_id=python_sw.id, cve_id="CVE-2023-24329", severity="MEDIUM",
            cvss_score=5.3, description="Startswith bypass in urlparse",
            published_date=date(2023, 2, 24), fixed_version="3.8.17"),
        Cve(software_id=node.id, cve_id="CVE-2023-30581", severity="HIGH",
            cvss_score=8.8, description="Path traversal bypass in ESM",
            published_date=date(2023, 6, 14), fixed_version="14.21.4"),
        Eol(software_id=openssl.id, version="1.1.1",
            release_date=date(2018, 9, 11), eol_date=date(2023, 9, 11), status="EOL"),
        Eol(software_id=python_sw.id, version="3.8",
            release_date=date(2019, 10, 14), eol_date=date(2024, 10, 14), status="EOL"),
        Eol(software_id=node.id, version="14",
            release_date=date(2020, 4, 21), eol_date=date(2023, 4, 30), status="EOL"),
    ])
    db.commit()
    print("เพิ่มข้อมูลตัวอย่างแล้ว")
else:
    print("มีข้อมูลอยู่แล้ว ข้ามการ seed")

db.close()