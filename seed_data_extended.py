from datetime import date
from db import SessionLocal
from models import Software, Cve, Eol

db = SessionLocal()

# ตรวจสอบว่ามีข้อมูลอยู่แล้วหรือไม่
if db.query(Software).count() > 0:
    print(f"มีข้อมูลอยู่แล้ว {db.query(Software).count()} รายการ")
    response = input("ต้องการเพิ่มข้อมูลอีก 50 รายการหรือไม่? (y/n): ")
    if response.lower() != 'y':
        db.close()
        exit()

# ข้อมูล Software 50 รายการ
softwares_data = [
    # Web Servers
    {"name": "Apache HTTP Server", "vendor": "Apache Software Foundation", "version": "2.4.54", "category": "Web Server", "os": "Linux", "ip": "192.168.1.101"},
    {"name": "Nginx", "vendor": "Nginx Inc", "version": "1.24.0", "category": "Web Server", "os": "Linux", "ip": "192.168.1.102"},
    {"name": "Microsoft IIS", "vendor": "Microsoft", "version": "10.0", "category": "Web Server", "os": "Windows Server 2022", "ip": "192.168.1.103"},
    
    # Databases
    {"name": "MySQL", "vendor": "Oracle", "version": "8.0.33", "category": "Database", "os": "Linux", "ip": "192.168.1.104"},
    {"name": "PostgreSQL", "vendor": "PostgreSQL Global Development Group", "version": "15.3", "category": "Database", "os": "Linux", "ip": "192.168.1.105"},
    {"name": "MongoDB", "vendor": "MongoDB Inc", "version": "6.0.8", "category": "Database", "os": "Linux", "ip": "192.168.1.106"},
    {"name": "Redis", "vendor": "Redis Labs", "version": "7.0.12", "category": "Database", "os": "Linux", "ip": "192.168.1.107"},
    {"name": "Microsoft SQL Server", "vendor": "Microsoft", "version": "2022", "category": "Database", "os": "Windows Server 2022", "ip": "192.168.1.108"},
    {"name": "Oracle Database", "vendor": "Oracle", "version": "19c", "category": "Database", "os": "Linux", "ip": "192.168.1.109"},
    {"name": "MariaDB", "vendor": "MariaDB Foundation", "version": "10.11.4", "category": "Database", "os": "Linux", "ip": "192.168.1.110"},
    
    # Programming Languages & Runtimes
    {"name": "Java", "vendor": "Oracle", "version": "17.0.7", "category": "Runtime", "os": "Windows Server 2022", "ip": "192.168.1.111"},
    {"name": "PHP", "vendor": "PHP Group", "version": "8.2.8", "category": "Runtime", "os": "Linux", "ip": "192.168.1.112"},
    {"name": "Ruby", "vendor": "Ruby Core Team", "version": "3.2.2", "category": "Runtime", "os": "Linux", "ip": "192.168.1.113"},
    {"name": "Go", "vendor": "Google", "version": "1.20.6", "category": "Runtime", "os": "Linux", "ip": "192.168.1.114"},
    {"name": "Rust", "vendor": "Rust Foundation", "version": "1.71.0", "category": "Runtime", "os": "Linux", "ip": "192.168.1.115"},
    {"name": "C#", "vendor": "Microsoft", "version": "11.0", "category": "Runtime", "os": "Windows 11", "ip": "192.168.1.116"},
    {"name": "TypeScript", "vendor": "Microsoft", "version": "5.1.6", "category": "Runtime", "os": "Windows 11", "ip": "192.168.1.117"},
    
    # Frameworks & Libraries
    {"name": "Django", "vendor": "Django Software Foundation", "version": "4.2.3", "category": "Framework", "os": "Linux", "ip": "192.168.1.118"},
    {"name": "Flask", "vendor": "Pallets Projects", "version": "2.3.2", "category": "Framework", "os": "Linux", "ip": "192.168.1.119"},
    {"name": "Spring Boot", "vendor": "VMware", "version": "3.1.2", "category": "Framework", "os": "Linux", "ip": "192.168.1.120"},
    {"name": "React", "vendor": "Meta", "version": "18.2.0", "category": "Framework", "os": "Windows 11", "ip": "192.168.1.121"},
    {"name": "Angular", "vendor": "Google", "version": "16.1.4", "category": "Framework", "os": "Windows 11", "ip": "192.168.1.122"},
    {"name": "Vue.js", "vendor": "Evan You", "version": "3.3.4", "category": "Framework", "os": "Windows 11", "ip": "192.168.1.123"},
    {"name": "Express.js", "vendor": "OpenJS Foundation", "version": "4.18.2", "category": "Framework", "os": "Linux", "ip": "192.168.1.124"},
    {"name": "jQuery", "vendor": "OpenJS Foundation", "version": "3.7.0", "category": "Library", "os": "Windows 11", "ip": "192.168.1.125"},
    {"name": "Lodash", "vendor": "JS Foundation", "version": "4.17.21", "category": "Library", "os": "Windows 11", "ip": "192.168.1.126"},
    {"name": "Bootstrap", "vendor": "Bootstrap Team", "version": "5.3.1", "category": "Library", "os": "Windows 11", "ip": "192.168.1.127"},
    
    # CMS & Platforms
    {"name": "WordPress", "vendor": "WordPress Foundation", "version": "6.3", "category": "CMS", "os": "Linux", "ip": "192.168.1.128"},
    {"name": "Drupal", "vendor": "Drupal Association", "version": "10.1.3", "category": "CMS", "os": "Linux", "ip": "192.168.1.129"},
    {"name": "Joomla", "vendor": "Open Source Matters", "version": "4.3.3", "category": "CMS", "os": "Linux", "ip": "192.168.1.130"},
    
    # DevOps & Tools
    {"name": "Docker", "vendor": "Docker Inc", "version": "24.0.5", "category": "DevOps", "os": "Linux", "ip": "192.168.1.131"},
    {"name": "Kubernetes", "vendor": "CNCF", "version": "1.27.4", "category": "DevOps", "os": "Linux", "ip": "192.168.1.132"},
    {"name": "Jenkins", "vendor": "Jenkins Project", "version": "2.414", "category": "DevOps", "os": "Linux", "ip": "192.168.1.133"},
    {"name": "Git", "vendor": "Software Freedom Conservancy", "version": "2.41.0", "category": "DevOps", "os": "Windows 11", "ip": "192.168.1.134"},
    {"name": "GitLab", "vendor": "GitLab Inc", "version": "16.2.1", "category": "DevOps", "os": "Linux", "ip": "192.168.1.135"},
    {"name": "GitHub Actions", "vendor": "GitHub", "version": "latest", "category": "DevOps", "os": "Cloud", "ip": "192.168.1.136"},
    
    # Security & Networking
    {"name": "OpenSSH", "vendor": "OpenBSD Project", "version": "9.3p2", "category": "Security", "os": "Linux", "ip": "192.168.1.137"},
    {"name": "curl", "vendor": "curl.se", "version": "8.2.1", "category": "Security", "os": "Linux", "ip": "192.168.1.138"},
    {"name": "OpenVPN", "vendor": "OpenVPN Inc", "version": "2.6.5", "category": "Security", "os": "Linux", "ip": "192.168.1.139"},
    {"name": "Wireshark", "vendor": "Wireshark Foundation", "version": "4.0.6", "category": "Security", "os": "Windows 11", "ip": "192.168.1.140"},
    
    # Messaging & Streaming
    {"name": "RabbitMQ", "vendor": "VMware", "version": "3.12.4", "category": "Messaging", "os": "Linux", "ip": "192.168.1.141"},
    {"name": "Apache Kafka", "vendor": "Apache Software Foundation", "version": "3.5.1", "category": "Messaging", "os": "Linux", "ip": "192.168.1.142"},
    {"name": "Elasticsearch", "vendor": "Elastic", "version": "8.9.0", "category": "Search", "os": "Linux", "ip": "192.168.1.143"},
    {"name": "Logstash", "vendor": "Elastic", "version": "8.9.0", "category": "Search", "os": "Linux", "ip": "192.168.1.144"},
    {"name": "Kibana", "vendor": "Elastic", "version": "8.9.0", "category": "Search", "os": "Linux", "ip": "192.168.1.145"},
    
    # Cloud & Infrastructure
    {"name": "Terraform", "vendor": "HashiCorp", "version": "1.5.4", "category": "Infrastructure", "os": "Linux", "ip": "192.168.1.146"},
    {"name": "Ansible", "vendor": "Red Hat", "version": "2.15.2", "category": "Infrastructure", "os": "Linux", "ip": "192.168.1.147"},
    {"name": "Prometheus", "vendor": "CNCF", "version": "2.46.0", "category": "Monitoring", "os": "Linux", "ip": "192.168.1.148"},
    {"name": "Grafana", "vendor": "Grafana Labs", "version": "10.0.3", "category": "Monitoring", "os": "Linux", "ip": "192.168.1.149"},
    {"name": "Nagios", "vendor": "Nagios Enterprises", "version": "4.4.13", "category": "Monitoring", "os": "Linux", "ip": "192.168.1.150"},
]

# ข้อมูล CVE ตัวอย่างสำหรับ software แต่ละตัว
cves_data = {
    "Apache HTTP Server": [
        {"cve_id": "CVE-2023-25690", "severity": "CRITICAL", "cvss": 9.8, "desc": "HTTP Request Smuggling", "published": "2023-02-17", "fixed": "2.4.56"},
    ],
    "Nginx": [
        {"cve_id": "CVE-2023-44487", "severity": "HIGH", "cvss": 7.5, "desc": "HTTP/2 Rapid Reset Attack", "published": "2023-10-10", "fixed": "1.25.2"},
    ],
    "MySQL": [
        {"cve_id": "CVE-2023-22025", "severity": "HIGH", "cvss": 7.1, "desc": "MySQL Server vulnerability", "published": "2023-07-18", "fixed": "8.0.34"},
    ],
    "PostgreSQL": [
        {"cve_id": "CVE-2023-39417", "severity": "MEDIUM", "cvss": 5.9, "desc": "SQL injection via libpq", "published": "2023-08-09", "fixed": "15.4"},
    ],
    "MongoDB": [
        {"cve_id": "CVE-2023-36052", "severity": "HIGH", "cvss": 7.5, "desc": "MongoDB privilege escalation", "published": "2023-08-08", "fixed": "6.0.9"},
    ],
    "Redis": [
        {"cve_id": "CVE-2023-28856", "severity": "CRITICAL", "cvss": 9.0, "desc": "Redis Lua sandbox escape", "published": "2023-05-24", "fixed": "7.0.13"},
    ],
    "Java": [
        {"cve_id": "CVE-2023-22006", "severity": "HIGH", "cvss": 7.5, "desc": "Java SE vulnerability", "published": "2023-07-18", "fixed": "17.0.8"},
    ],
    "PHP": [
        {"cve_id": "CVE-2023-3823", "severity": "CRITICAL", "cvss": 9.8, "desc": "PHP object injection", "published": "2023-07-20", "fixed": "8.2.9"},
    ],
    "WordPress": [
        {"cve_id": "CVE-2023-38000", "severity": "HIGH", "cvss": 8.6, "desc": "WordPress privilege escalation", "published": "2023-08-08", "fixed": "6.3.1"},
    ],
    "Docker": [
        {"cve_id": "CVE-2023-28841", "severity": "HIGH", "cvss": 7.8, "desc": "Docker container escape", "published": "2023-05-24", "fixed": "24.0.6"},
    ],
    "Kubernetes": [
        {"cve_id": "CVE-2023-2727", "severity": "HIGH", "cvss": 8.0, "desc": "Kubernetes privilege escalation", "published": "2023-06-13", "fixed": "1.27.5"},
    ],
    "OpenSSH": [
        {"cve_id": "CVE-2023-38408", "severity": "CRITICAL", "cvss": 9.8, "desc": "OpenSSH remote code execution", "published": "2023-07-19", "fixed": "9.3p3"},
    ],
    "curl": [
        {"cve_id": "CVE-2023-38545", "severity": "HIGH", "cvss": 7.5, "desc": "curl SOCKS5 heap buffer overflow", "published": "2023-10-11", "fixed": "8.4.0"},
    ],
    "Elasticsearch": [
        {"cve_id": "CVE-2023-31418", "severity": "HIGH", "cvss": 7.5, "desc": "Elasticsearch information disclosure", "published": "2023-06-13", "fixed": "8.9.1"},
    ],
    "Jenkins": [
        {"cve_id": "CVE-2023-35152", "severity": "HIGH", "cvss": 8.8, "desc": "Jenkins CSRF vulnerability", "published": "2023-07-26", "fixed": "2.415"},
    ],
}

# ข้อมูล EOL สำหรับ software บางตัว
eols_data = {
    "Python": {"version": "3.8", "release": "2019-10-14", "eol": "2024-10-14", "status": "EOL"},
    "Node.js": {"version": "14", "release": "2020-04-21", "eol": "2023-04-30", "status": "EOL"},
    "OpenSSL": {"version": "1.1.1", "release": "2018-09-11", "eol": "2023-09-11", "status": "EOL"},
    "PHP": {"version": "7.4", "release": "2019-11-28", "eol": "2022-11-28", "status": "EOL"},
    "Java": {"version": "8", "release": "2014-03-18", "eol": "2022-01-01", "status": "EOL"},
    "Ubuntu": {"version": "18.04", "release": "2018-04-26", "eol": "2023-04-02", "status": "EOL"},
    "CentOS": {"version": "7", "release": "2014-07-07", "eol": "2024-06-30", "status": "EOL"},
    "Windows Server": {"version": "2012 R2", "release": "2013-10-18", "eol": "2023-10-10", "status": "EOL"},
}

print("กำลังเพิ่มข้อมูล Software 50 รายการ...")

added_count = 0
for idx, sw_data in enumerate(softwares_data, start=1):
    # สร้าง Software
    software = Software(
        name=sw_data["name"],
        vendor=sw_data["vendor"],
        version=sw_data["version"],
        category=sw_data["category"],
        operating_system=sw_data["os"],
        install_location=f"/opt/{sw_data['name'].lower().replace(' ', '-')}" if sw_data["os"] == "Linux" else f"C:\\Program Files\\{sw_data['name']}",
        ip_address=sw_data["ip"],
        last_scan_date=date.today(),
    )
    db.add(software)
    db.flush()
    
    # เพิ่ม CVE ถ้ามี
    if sw_data["name"] in cves_data:
        for cve_info in cves_data[sw_data["name"]]:
            cve = Cve(
                software_id=software.id,
                cve_id=cve_info["cve_id"],
                severity=cve_info["severity"],
                cvss_score=cve_info["cvss"],
                description=cve_info["desc"],
                published_date=date.fromisoformat(cve_info["published"]),
                fixed_version=cve_info["fixed"],
            )
            db.add(cve)
    
    # เพิ่ม EOL ถ้ามี
    if sw_data["name"] in eols_data:
        eol_info = eols_data[sw_data["name"]]
        eol = Eol(
            software_id=software.id,
            version=eol_info["version"],
            release_date=date.fromisoformat(eol_info["release"]),
            eol_date=date.fromisoformat(eol_info["eol"]),
            status=eol_info["status"],
        )
        db.add(eol)
    
    added_count += 1
    if idx % 10 == 0:
        print(f"  เพิ่มแล้ว {idx}/{len(softwares_data)} รายการ")

db.commit()
print(f"\n✅ เพิ่มข้อมูล Software สำเร็จ {added_count} รายการ")
print(f"📊 รวมข้อมูลทั้งหมด: {db.query(Software).count()} รายการ")

db.close()