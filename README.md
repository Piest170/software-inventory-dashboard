# ️ MAISON ICD - Software Inventory Dashboard

Dashboard สำหรับจัดการ Software Inventory พร้อมติดตาม **CVE** (Common Vulnerabilities and Exposures) และ **EOL** (End of Life) ออกแบบด้วยธีม Cyberpunk ตาม Corporate Identity ของ MAISON ICD

![MAISON ICD](https://img.shields.io/badge/MAISON_ICD-Cyberpunk_Theme-00F3FF?style=for-the-badge&logo=shield&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL_Server-2025-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)

---

## 📸 Screenshots

| Dashboard | Register Software |
|-----------|-------------------|
| หน้าหลักแสดง KPI, ตาราง Software, Search & Filter | ฟอร์มลงทะเบียน Software ใหม่พร้อม Live Preview |

---

## ✨ Features

### 🎯 Core Features
- ✅ **Dashboard** - แสดงภาพรวม Software Inventory พร้อม KPI Cards 5 มิติ
- ✅ **CVE Tracking** - ติดตามช่องโหว่ความปลอดภัย (Critical, High, Medium, Low)
- ✅ **EOL Monitoring** - ตรวจสอบสถานะ End of Life ของ Software
- ✅ **Register Software** - ลงทะเบียน Software ใหม่พร้อม Live Preview
- ✅ **Search & Filter** - ค้นหาตามชื่อ, ผู้ผลิต, เวอร์ชัน, OS, IP
- ✅ **Pagination** - แบ่งหน้าอัตโนมัติ (10 รายการ/หน้า)
- ✅ **REST API** - API JSON สำหรับ integrate กับระบบอื่น

### 🎨 UI/UX Features
- ✅ **Cyberpunk Theme** - ธีม MAISON ICD สไตล์ futuristic
- ✅ **Particle Animation** - พื้นหลังอนุภาคเคลื่อนไหวแบบ real-time
- ✅ **Grid Background** - พื้นหลังตารางเคลื่อนที่
- ✅ **Neon Glow Effects** - เอฟเฟกต์แสงนีออน
- ✅ **Smooth Animations** - fade-in, slide-in, counter animation
- ✅ **Responsive Design** - รองรับทุกขนาดหน้าจอ
- ✅ **Live Preview** - แสดงข้อมูลแบบ real-time ขณะกรอกฟอร์ม
- ✅ **Form Validation** - ตรวจสอบข้อมูลก่อน submit

### 📊 KPI Metrics
| KPI | คำอธิบาย | สี |
|-----|----------|-----|
| Software ทั้งหมด | จำนวน Software ในระบบ | 🔵 Cyan |
| CVE ทั้งหมด | จำนวน CVE ทั้งหมด | 🔵 Blue |
| Critical CVE | จำนวน CVE ระดับ Critical |  Red |
| EOL แล้ว | จำนวนที่หมดอายุซัพพอร์ต | 🟠 Orange |
| ไม่ระบุ | จำนวนที่ยังไม่มีข้อมูล EOL | ⚫ Gray |

---

## 🛠️ Tech Stack

### Backend
- **Python 3.14** - Programming Language
- **FastAPI 0.141** - Web Framework (async, high-performance)
- **SQLAlchemy 2.0** - ORM สำหรับจัดการ Database
- **pyodbc** - Driver เชื่อมต่อ SQL Server
- **python-dotenv** - จัดการ Environment Variables
- **python-multipart** - รองรับ Form Data

### Database
- **Microsoft SQL Server 2025** - Local Database (SQLEXPRESS)
- **ODBC Driver 18** - Database Connector

### Frontend
- **Jinja2** - Template Engine
- **Bootstrap 5.3** - CSS Framework
- **Orbitron Font** - Cyberpunk Font
- **Rajdhani Font** - Body Font
- **Vanilla JavaScript** - Particle Animation, Counter Animation

### Tools
- **Git** - Version Control
- **VS Code** - Code Editor
- **uvicorn** - ASGI Server

---

## 📋 Prerequisites

ก่อนติดตั้ง ต้องมีสิ่งเหล่านี้ในเครื่อง:

1. **Python 3.12+** - [ดาวน์โหลด](https://www.python.org/downloads/)
2. **Microsoft SQL Server 2025** (หรือ 2022) - [ดาวน์โหลด](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
3. **ODBC Driver 18 for SQL Server** - [ดาวน์โหลด](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
4. **Git** - [ดาวน์โหลด](https://git-scm.com/download/win)

---