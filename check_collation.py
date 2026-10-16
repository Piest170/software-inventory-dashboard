import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
server = os.getenv("DB_SERVER", r"localhost\SQLEXPRESS")
database = os.getenv("DB_NAME", "SoftwareInventory")

conn_str = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
    "Encrypt=no;"
    "TrustServerCertificate=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # ตรวจสอบ Collation ของ Database
    cursor.execute("SELECT DATABASEPROPERTYEX('SoftwareInventory', 'Collation') AS DatabaseCollation")
    result = cursor.fetchone()
    print(f"Database Collation: {result[0]}")
    
    # ตรวจสอบ Collation ของ Table Software
    cursor.execute("""
        SELECT COLUMN_NAME, COLLATION_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'Software' 
        AND COLLATION_NAME IS NOT NULL
    """)
    print("\nColumn Collations in 'Software' table:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")
    
    # ทดสอบค้นหาแบบ case-sensitive
    print("\n--- ทดสอบค้นหา 'X' (ตัวใหญ่) ---")
    cursor.execute("SELECT name FROM Software WHERE name LIKE '%X%'")
    for row in cursor.fetchall():
        print(f"  Found: {row[0]}")
    
    print("\n--- ทดสอบค้นหา 'x' (ตัวเล็ก) ---")
    cursor.execute("SELECT name FROM Software WHERE name LIKE '%x%'")
    for row in cursor.fetchall():
        print(f"  Found: {row[0]}")
    
    print("\n--- ทดสอบค้นหาด้วย LOWER() ---")
    cursor.execute("SELECT name FROM Software WHERE LOWER(name) LIKE '%x%'")
    for row in cursor.fetchall():
        print(f"  Found: {row[0]}")
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")