import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()


def _bool_env(name: str, default: str = "false") -> bool:
    value = os.getenv(name, default)
    return value.strip().lower() in ("1", "true", "yes", "y")


def build_odbc_connection_string() -> str:
    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    server = os.getenv("DB_SERVER", "localhost")
    database = os.getenv("DB_NAME", "SoftwareInventory")

    windows_auth = _bool_env("USE_WINDOWS_AUTH", "true")
    user = os.getenv("DB_USER", "")
    password = os.getenv("DB_PASSWORD", "")

    encrypt = _bool_env("DB_ENCRYPT", "false")
    trust_cert = _bool_env("DB_TRUST_SERVER_CERTIFICATE", "true")

    parts = [
        f"DRIVER={{{driver}}}",
        f"SERVER={server}",
        f"DATABASE={database}",
    ]

    if windows_auth:
        parts.append("Trusted_Connection=yes")
    else:
        parts.append(f"UID={user}")
        parts.append(f"PWD={password}")

    parts.append(f"Encrypt={'yes' if encrypt else 'no'}")
    parts.append(f"TrustServerCertificate={'yes' if trust_cert else 'no'}")

    return ";".join(parts)


CONNECTION_STRING = build_odbc_connection_string()
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc:///?odbc_connect=" + quote_plus(CONNECTION_STRING)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()