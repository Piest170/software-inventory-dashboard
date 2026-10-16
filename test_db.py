import pyodbc
from db import CONNECTION_STRING

def main():
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        result = cursor.execute("SELECT @@VERSION").fetchone()
        print("เชื่อมต่อ SQL Server สำเร็จ")
        print(result[0])

    except Exception as e:
        print("เชื่อมต่อไม่สำเร็จ")
        print(e)


if __name__ == "__main__":
    main()