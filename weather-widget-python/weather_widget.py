# ============================================================
# weather_widget.py
# WeatherWidget ใช้ Card เป็นฐาน แล้วใส่ข้อมูลอากาศลงใน card.body
# สังเกต: ไม่มีพารามิเตอร์ theme เลย แต่สีก็เปลี่ยนตามธีมได้
# เพราะ Card อ่านจาก Context เอง
# ============================================================
import tkinter as tk
from card import Card


class WeatherWidget(Card):
    def __init__(self, parent, city, temp, condition, humidity):
        super().__init__(parent, title=city)  # ใช้ชื่อจังหวัดเป็น title ของการ์ด

        # ใส่เนื้อหาลงใน body (เทียบเท่า children)
        tk.Label(self.body, text=f"{temp}°C", font=("Helvetica", 28, "bold")).pack(anchor="w")
        tk.Label(self.body, text=condition).pack(anchor="w")
        tk.Label(self.body, text=f"ความชื้น {humidity}%", font=("Helvetica", 10)).pack(anchor="w")

        # ทาสีอีกรอบ เพราะเพิ่งเพิ่ม Label ใหม่เข้าไปหลังจาก Card ทาสีครั้งแรกไปแล้ว
        self.apply_theme(self.theme.theme)
