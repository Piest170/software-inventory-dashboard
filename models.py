from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Numeric,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from db import Base


class Software(Base):
    __tablename__ = "Software"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    vendor = Column(String(200), nullable=True)
    version = Column(String(100), nullable=True)
    category = Column(String(100), nullable=True)
    operating_system = Column(String(100), nullable=True)
    install_location = Column(String(500), nullable=True)
    ip_address = Column(String(45), nullable=True)
    last_scan_date = Column(Date, nullable=True)

    cves = relationship("Cve", back_populates="software", cascade="all, delete-orphan")
    eols = relationship("Eol", back_populates="software", cascade="all, delete-orphan")


class Cve(Base):
    __tablename__ = "Cve"

    id = Column(Integer, primary_key=True)
    software_id = Column(Integer, ForeignKey("Software.id"), nullable=False)
    cve_id = Column(String(20), nullable=False, index=True)
    severity = Column(String(20), nullable=True)
    cvss_score = Column(Numeric(3, 1), nullable=True)
    description = Column(String(2000), nullable=True)
    published_date = Column(Date, nullable=True)
    fixed_version = Column(String(100), nullable=True)

    software = relationship("Software", back_populates="cves")


class Eol(Base):
    __tablename__ = "Eol"

    id = Column(Integer, primary_key=True)
    software_id = Column(Integer, ForeignKey("Software.id"), nullable=False)
    version = Column(String(100), nullable=True)
    release_date = Column(Date, nullable=True)
    eol_date = Column(Date, nullable=True)
    status = Column(String(50), nullable=True)

    software = relationship("Software", back_populates="eols")