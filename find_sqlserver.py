import pyodbc

candidates = [
    r"localhost",
    r"(localdb)\MSSQLLocalDB",
    r"localhost\SQLEXPRESS",
    r".\SQLEXPRESS",
]

for server in candidates:
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={server};"
        "DATABASE=master;"
        "Trusted_Connection=yes;"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )
    try:
        conn = pyodbc.connect(conn_str, timeout=5)
        version = conn.cursor().execute("SELECT @@VERSION").fetchone()[0]
        print(f"[OK]   {server}")
        print("       ", version.splitlines()[0])
        conn.close()
    except Exception as e:
        print(f"[FAIL] {server} -> {type(e).__name__}: {e}")