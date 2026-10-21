# ============================================================
# app.py  (เทียบเท่า App.jsx)  รันด้วย:  python app.py
# สร้าง ThemeProvider เพียงครั้งเดียว แล้วทุกคอมโพเนนต์ใช้ use_theme() ได้เอง
# ไม่มีการส่ง theme เป็นพารามิเตอร์ไปที่ WeatherWidget เลย
# ============================================================
import tkinter as tk
from theme_context import ThemeProvider, use_theme
from theme_toggle import ThemeToggle
from weather_widget import WeatherWidget
from clock_widget import ClockWidget
from quote_widget import QuoteWidget

# ข้อมูลอากาศจำลองของหลายจังหวัด (ของจริงอาจดึงจาก API)
PROVINCES = [
    {"city": "กรุงเทพฯ", "temp": 34, "condition": "☀️ แดดจัด", "humidity": 60},
    {"city": "เชียงใหม่", "temp": 29, "condition": "⛅ มีเมฆบางส่วน", "humidity": 70},
    {"city": "ภูเก็ต", "temp": 31, "condition": "🌧️ ฝนตก", "humidity": 85},
    {"city": "นครปฐม", "temp": 33, "condition": "🌤️ แดดบางส่วน", "humidity": 65},
]


def main():
    # 1) ห่อทั้งแอปด้วย ThemeProvider (เทียบเท่า <ThemeProvider> ใน App.jsx)
    ThemeProvider()
    theme = use_theme()

    root = tk.Tk()
    root.title("Weather Widget")
    root.geometry("760x420")

    # พื้นหลังของหน้า ก็ subscribe ธีมเหมือนกัน
    root.configure(padx=24, pady=24)
    theme.subscribe(lambda name: root.configure(bg=theme.colors()["page_bg"]))

    ThemeToggle(root).pack(anchor="w")

    # กล่องวาง Widget แบบตาราง
    container = tk.Frame(root)
    container.pack(anchor="w", pady=24)
    theme.subscribe(lambda name: container.configure(bg=theme.colors()["page_bg"]))

    widgets = [WeatherWidget(container, **p) for p in PROVINCES]
    widgets += [ClockWidget(container), QuoteWidget(container)]

    # จัดวาง 3 คอลัมน์
    for i, w in enumerate(widgets):
        w.grid(row=i // 3, column=i % 3, padx=8, pady=8, sticky="n")

    root.mainloop()


if __name__ == "__main__":
    main()
