from typing import Optional
from datetime import date
import math

from fastapi import FastAPI, Depends, Request, Query, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func, distinct

from db import get_db, engine, Base
from models import Software, Cve, Eol


Base.metadata.create_all(bind=engine)

app = FastAPI(title="MAISON ICD - Software Inventory Dashboard")
templates = Jinja2Templates(directory="templates")

ITEMS_PER_PAGE = 10


@app.get("/")
def dashboard(
    request: Request,
    q: str = Query(default=""),
    severity: str = Query(default=""),
    eol: str = Query(default=""),
    page: int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
):
    today = date.today()
    q = q.strip()

    # ถ้ามีการค้นหาใหม่ ให้รีเซ็ตไปหน้า 1
    if q or severity or eol:
        page = 1

    # Base query สำหรับ count
    base_query = db.query(Software.id)

    if q:
        lower_q = q.lower()
        pattern = f"%{lower_q}%"
        base_query = base_query.filter(
            or_(
                func.lower(Software.name).like(pattern),
                func.lower(Software.vendor).like(pattern),
                func.lower(Software.version).like(pattern),
                func.lower(Software.category).like(pattern),
                func.lower(Software.operating_system).like(pattern),
                func.lower(Software.ip_address).like(pattern),
            )
        )

    if severity:
        base_query = base_query.join(Cve).filter(
            func.upper(Cve.severity) == severity.upper()
        ).distinct()

    if eol == "eol":
        base_query = base_query.join(Eol).filter(
            Eol.eol_date < today
        ).distinct()
    elif eol == "supported":
        base_query = base_query.join(Eol).filter(
            Eol.eol_date >= today
        ).distinct()
    elif eol == "not_specified":
        base_query = base_query.filter(
            ~Software.id.in_(db.query(Eol.software_id).distinct())
        )

    total_items = base_query.count()
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE) if total_items > 0 else 1
    page = max(1, min(page, total_pages))

    # Query หลัก
    query = db.query(Software).options(
        joinedload(Software.cves),
        joinedload(Software.eols),
    )

    if q:
        lower_q = q.lower()
        pattern = f"%{lower_q}%"
        query = query.filter(
            or_(
                func.lower(Software.name).like(pattern),
                func.lower(Software.vendor).like(pattern),
                func.lower(Software.version).like(pattern),
                func.lower(Software.category).like(pattern),
                func.lower(Software.operating_system).like(pattern),
                func.lower(Software.ip_address).like(pattern),
            )
        )

    if severity:
        query = query.join(Software.cves).filter(
            func.upper(Cve.severity) == severity.upper()
        ).distinct()

    if eol == "eol":
        query = query.join(Software.eols).filter(
            Eol.eol_date < today
        ).distinct()
    elif eol == "supported":
        query = query.join(Software.eols).filter(
            Eol.eol_date >= today
        ).distinct()
    elif eol == "not_specified":
        query = query.filter(
            ~Software.id.in_(db.query(Eol.software_id).distinct())
        )

    offset = (page - 1) * ITEMS_PER_PAGE
    softwares = query.order_by(Software.name).offset(offset).limit(ITEMS_PER_PAGE).all()

    total_software = db.query(func.count(Software.id)).scalar() or 0
    total_cve = db.query(func.count(Cve.id)).scalar() or 0
    critical_cve = db.query(func.count(Cve.id)).filter(
        func.upper(Cve.severity) == "CRITICAL"
    ).scalar() or 0
    high_cve = db.query(func.count(Cve.id)).filter(
        func.upper(Cve.severity) == "HIGH"
    ).scalar() or 0
    eol_count = db.query(func.count(Eol.id)).filter(
        Eol.eol_date < today
    ).scalar() or 0
    
    # จำนวน Software ที่มีข้อมูล EOL ระบุไว้
    has_eol_count = db.query(func.count(distinct(Eol.software_id))).scalar() or 0
    
    # จำนวน Software ที่ไม่มีข้อมูล EOL (ไม่ระบุ)
    not_specified_count = total_software - has_eol_count

    start_item = offset + 1 if total_items > 0 else 0
    end_item = min(offset + ITEMS_PER_PAGE, total_items)

    pagination_pages = []
    if total_pages <= 7:
        pagination_pages = list(range(1, total_pages + 1))
    else:
        if page <= 4:
            pagination_pages = [1, 2, 3, 4, 5, "...", total_pages]
        elif page >= total_pages - 3:
            pagination_pages = [1, "...", total_pages - 4, total_pages - 3, total_pages - 2, total_pages - 1, total_pages]
        else:
            pagination_pages = [1, "...", page - 1, page, page + 1, "...", total_pages]

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "softwares": softwares,
            "q": q,
            "severity": severity,
            "eol": eol,
            "today": today,
            "stats": {
                "total_software": total_software,
                "total_cve": total_cve,
                "critical_cve": critical_cve,
                "high_cve": high_cve,
                "eol_count": eol_count,
                "has_eol_count": has_eol_count,
                "not_specified_count": not_specified_count,
            },
            "pagination": {
                "page": page,
                "total_pages": total_pages,
                "total_items": total_items,
                "per_page": ITEMS_PER_PAGE,
                "start_item": start_item,
                "end_item": end_item,
                "pages": pagination_pages,
                "has_prev": page > 1,
                "has_next": page < total_pages,
                "prev_page": page - 1,
                "next_page": page + 1,
            },
        },
    )


@app.get("/software/{software_id}")
def software_detail(
    software_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    software = (
        db.query(Software)
        .options(
            joinedload(Software.cves),
            joinedload(Software.eols),
        )
        .filter(Software.id == software_id)
        .first()
    )

    if not software:
        raise HTTPException(status_code=404, detail="Software not found")

    return templates.TemplateResponse(
        request=request,
        name="software_detail.html",
        context={
            "software": software,
            "today": date.today(),
        },
    )


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "today": date.today(),
            "message": None,
            "message_type": None,
        },
    )


@app.post("/register", response_class=HTMLResponse)
def register_submit(
    request: Request,
    name: str = Form(...),
    vendor: str = Form(...),
    version: str = Form(...),
    category: str = Form(...),
    operating_system: str = Form(...),
    install_location: str = Form(""),
    ip_address: str = Form(""),
    db: Session = Depends(get_db),
):
    try:
        new_software = Software(
            name=name.strip(),
            vendor=vendor.strip(),
            version=version.strip(),
            category=category.strip(),
            operating_system=operating_system.strip(),
            install_location=install_location.strip() if install_location else None,
            ip_address=ip_address.strip() if ip_address else None,
            last_scan_date=date.today(),
        )
        db.add(new_software)
        db.commit()
        db.refresh(new_software)

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "today": date.today(),
                "message": f"✅ เพิ่ม Software '{name}' สำเร็จ (ID: {new_software.id})",
                "message_type": "success",
                "submitted": {
                    "name": name,
                    "vendor": vendor,
                    "version": version,
                    "category": category,
                    "operating_system": operating_system,
                    "install_location": install_location,
                    "ip_address": ip_address,
                },
            },
        )
    except Exception as e:
        db.rollback()
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "today": date.today(),
                "message": f" เกิดข้อผิดพลาด: {str(e)}",
                "message_type": "error",
            },
        )


@app.get("/api/software")
def api_software(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=100),
):
    query = db.query(Software).options(
        joinedload(Software.cves),
        joinedload(Software.eols),
    )

    if q:
        lower_q = q.strip().lower()
        pattern = f"%{lower_q}%"
        query = query.filter(
            or_(
                func.lower(Software.name).like(pattern),
                func.lower(Software.vendor).like(pattern),
                func.lower(Software.version).like(pattern),
                func.lower(Software.category).like(pattern),
                func.lower(Software.operating_system).like(pattern),
                func.lower(Software.ip_address).like(pattern),
            )
        )

    total = query.count()
    offset = (page - 1) * per_page
    software_list = query.order_by(Software.name).offset(offset).limit(per_page).all()

    result = []
    for s in software_list:
        eol_dates = [e.eol_date for e in s.eols if e.eol_date]
        latest_eol = max(eol_dates) if eol_dates else None

        result.append({
            "id": s.id,
            "name": s.name,
            "vendor": s.vendor,
            "version": s.version,
            "category": s.category,
            "operating_system": s.operating_system,
            "last_scan_date": s.last_scan_date,
            "cve_count": len(s.cves),
            "critical_cve_count": len([
                c for c in s.cves
                if (c.severity or "").upper() == "CRITICAL"
            ]),
            "latest_eol_date": latest_eol,
            "is_eol": bool(latest_eol and latest_eol < date.today()),
        })

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": math.ceil(total / per_page) if total > 0 else 1,
        "items": result,
    }