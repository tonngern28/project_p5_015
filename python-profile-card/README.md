# Mini Project: ProfileCard (เวอร์ชัน Python)

## วิธีรัน
1. ติดตั้ง Python 3.8 ขึ้นไป (ตรวจด้วย: python --version)
2. เปิดเทอร์มินัลในโฟลเดอร์นี้ แล้วรัน
   python app.py
3. เบราว์เซอร์จะเปิดหน้าเว็บให้อัตโนมัติ (หรือเปิดไฟล์ output/index.html เอง)

ไม่ต้องติดตั้งไลบรารีเพิ่ม (ใช้เฉพาะโมดูลมาตรฐานของ Python)

## โครงสร้างไฟล์
├── app.py                    ไฟล์หลัก ใช้ ProfileCard 4 ครั้ง แล้วสร้างเว็บ
├── components/
│   ├── profile_card.py       คอมโพเนนต์ ProfileCard (รับ props 4 ตัว + theme)
│   └── profile_card.css      สไตล์ของการ์ด
├── static/
│   ├── app.css               สไตล์หน้าหลักและปุ่มสลับโหมด
│   └── script.js             ปุ่มทักทาย (alert) และปุ่มสลับโหมด
└── output/                   เว็บที่ Python สร้างให้ (เกิดหลังรัน app.py)

## หลักการสำคัญ
- Component: ProfileCard คือฟังก์ชันที่คืนค่า HTML ใช้ซ้ำได้หลายครั้ง
- Props: พารามิเตอร์ name, role, emoji, color (และ theme)
- ไม่มี inline style: Python แปลงรหัสสีเป็นชื่อคลาส แล้วสร้างไฟล์ colors.css ให้
