import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
server = os.getenv("DB_SERVER", r"localhost\SQLEXPRESS")
database = os.getenv("DB_NAME", "SoftwareInventory")

master_conn_str = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    "DATABASE=master;"
    "Trusted_Connection=yes;"
    "Encrypt=no;"
    "TrustServerCertificate=yes;"
)

conn = pyodbc.connect(master_conn_str, autocommit=True)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM sys.databases WHERE name = ?", database)

if cursor.fetchone()[0] == 0:
    cursor.execute(f"CREATE DATABASE [{database}]")
    print(f"สร้าง database '{database}' เรียบร้อย")
else:
    print(f"มี database '{database}' อยู่แล้ว")

conn.close()

from db import engine, Base
import models  # noqa: F401  # เพื่อให้ Base รู้จักตารางทั้ง 3

Base.metadata.create_all(bind=engine)
print("สร้างตาราง Software / Cve / Eol เรียบร้อย")