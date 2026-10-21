# ==========================================================
# app.py - ไฟล์หลัก (เทียบเท่า App.jsx ในเวอร์ชัน React)
# หน้าที่: ใช้ ProfileCard 4 ครั้ง แล้วสร้างเว็บไซต์ไว้ในโฟลเดอร์ output/
# วิธีรัน: python app.py
# ==========================================================

# ขั้นที่ 1: นำเข้าโมดูลที่ใช้
import shutil                    # คัดลอกไฟล์
import webbrowser                # เปิดเบราว์เซอร์อัตโนมัติ
from pathlib import Path         # จัดการเส้นทางไฟล์

# นำเข้าคอมโพเนนต์ ProfileCard และฟังก์ชันสร้าง CSS ของสี
from components.profile_card import ProfileCard, color_css

# ขั้นที่ 2: กำหนดโฟลเดอร์ต่างๆ (อ้างอิงจากตำแหน่งของไฟล์นี้)
# .resolve() แปลงเป็นพาธเต็ม (absolute) เพื่อให้ as_uri() ใช้เปิดเบราว์เซอร์ได้เสมอ
BASE = Path(__file__).resolve().parent
OUT = BASE / "output"            # โฟลเดอร์ที่เก็บเว็บไซต์ที่สร้างเสร็จ

# ขั้นที่ 3: ข้อมูลสมาชิก 4 คน (ข้อมูลและสีแตกต่างกัน)
# แต่ละรายการคือชุด props ที่ส่งให้ ProfileCard
members = [
    dict(name="สมชาย",  role="หัวหน้าชมรม",       emoji="🎮", color="#ff6b6b"),
    dict(name="สมหญิง", role="รองหัวหน้า",         emoji="🎨", color="#4dabf7"),
    dict(name="ปราณี",  role="เหรัญญิก",          emoji="📚", color="#51cf66"),
    dict(name="วิชัย",   role="ฝ่ายประชาสัมพันธ์", emoji="📸", color="#9775fa"),
]

# ขั้นที่ 4: เรียกใช้ ProfileCard ซ้ำทุกคนในรายการ แล้วต่อ HTML เข้าด้วยกัน
# **m คือการกระจาย dict เป็นพารามิเตอร์ (name=..., role=..., ...)
cards_html = "\n".join(ProfileCard(**m) for m in members)

# ขั้นที่ 5: ประกอบหน้า HTML ทั้งหน้า
# - ลิงก์ไฟล์ CSS/JS แยกไฟล์ (ไม่มี inline style และไม่มี inline script)
# - class "app app--light" คือหน้าหลักเริ่มต้นเป็นโหมดสว่าง
html = f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Open House - ProfileCard</title>
  <link rel="stylesheet" href="profile_card.css">
  <link rel="stylesheet" href="colors.css">
  <link rel="stylesheet" href="app.css">
</head>
<body>
  <div class="app app--light">
    <header class="app__header">
      <h1>สมาชิกชมรม - Open House</h1>
      <button class="theme-toggle">🌙 โหมดมืด</button>
    </header>
    <div class="card-list">
      {cards_html}
    </div>
  </div>
  <script src="script.js"></script>
</body>
</html>"""

# ขั้นที่ 6: เขียนไฟล์ทั้งหมดลงโฟลเดอร์ output/
OUT.mkdir(exist_ok=True)                                          # สร้างโฟลเดอร์ถ้ายังไม่มี
(OUT / "index.html").write_text(html, encoding="utf-8")           # หน้าเว็บหลัก
(OUT / "colors.css").write_text(                                  # CSS ของสีทุกใบ (สร้างจากโค้ด)
    color_css(m["color"] for m in members), encoding="utf-8"
)
shutil.copy(BASE / "components" / "profile_card.css", OUT / "profile_card.css")
shutil.copy(BASE / "static" / "app.css", OUT / "app.css")
shutil.copy(BASE / "static" / "script.js", OUT / "script.js")

# ขั้นที่ 7: แจ้งผลและเปิดเว็บในเบราว์เซอร์
print("สร้างเว็บไซต์สำเร็จที่:", OUT / "index.html")
webbrowser.open((OUT / "index.html").as_uri())
