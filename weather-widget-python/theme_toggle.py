# ============================================================
# theme_toggle.py
# ปุ่มสลับโหมดสว่าง/มืด อ่านค่าและเรียก toggle_theme จาก Context โดยตรง
# ============================================================
import tkinter as tk
from theme_context import use_theme


class ThemeToggle(tk.Button):
    def __init__(self, parent):
        self.theme = use_theme()
        # command = ฟังก์ชันที่จะถูกเรียกเมื่อกดปุ่ม
        super().__init__(parent, command=self.theme.toggle_theme, font=("Helvetica", 12), padx=12, pady=6)
        self.theme.subscribe(self._update_text)
        self.bind("<Destroy>", lambda e: self.theme.unsubscribe(self._update_text) if e.widget is self else None)

    def _update_text(self, theme_name):
        """เปลี่ยนข้อความบนปุ่มตามธีมปัจจุบัน"""
        self.configure(text="🌙 เปลี่ยนเป็นโหมดมืด" if theme_name == "light" else "☀️ เปลี่ยนเป็นโหมดสว่าง")
