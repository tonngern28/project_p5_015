# ============================================================
# card.py
# คอมโพเนนต์ Card ที่:
#   - รับ title และมี "body" ให้ใส่เนื้อหาอะไรก็ได้ (Composition Pattern)
#   - อ่าน theme จาก Context (use_theme) โดยตรง ไม่รับ theme ผ่านพารามิเตอร์
# ============================================================
import tkinter as tk
from theme_context import use_theme


class Card(tk.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, bd=1, relief="solid", padx=16, pady=16)

        # ดึง Provider จาก Context โดยตรง (ไม่มี props drilling)
        self.theme = use_theme()

        # ส่วนหัวของการ์ด
        self.title_label = tk.Label(self, text=title, font=("Helvetica", 14, "bold"), anchor="w")
        self.title_label.pack(fill="x")

        # body = พื้นที่ว่างสำหรับใส่ "children" (เทียบเท่า {children} ใน React)
        # คอมโพเนนต์ลูกใช้ parent=card.body เพื่อใส่เนื้อหาอะไรก็ได้
        self.body = tk.Frame(self)
        self.body.pack(fill="both", expand=True, pady=(8, 0))

        # สมัครรับการแจ้งเตือนเมื่อธีมเปลี่ยน (และถูกเรียกครั้งแรกทันที)
        self.theme.subscribe(self.apply_theme)
        # เมื่อการ์ดถูกทำลาย ให้เลิกติดตาม ป้องกัน error
        self.bind("<Destroy>", self._on_destroy)

    def apply_theme(self, theme_name):
        """ทาสีการ์ดและทุกอย่างที่อยู่ข้างในใหม่ตามธีม"""
        c = self.theme.colors()
        self.configure(bg=c["card_bg"], highlightbackground=c["border"])
        self._paint(self, c)

    def _paint(self, widget, c):
        """วนทาสีลูกทุกตัวแบบ recursive ทำให้เนื้อหาที่ใส่เข้ามาเปลี่ยนสีตามอัตโนมัติ"""
        for child in widget.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(bg=c["card_bg"], fg=c["text"])
            elif isinstance(child, tk.Frame):
                child.configure(bg=c["card_bg"])
            self._paint(child, c)
        if isinstance(widget, tk.Label):
            widget.configure(bg=c["card_bg"], fg=c["text"])

    def _on_destroy(self, event):
        # event.widget คือตัวที่ถูกทำลาย (ลูกก็ส่ง event นี้ขึ้นมา จึงต้องเช็คว่าเป็นตัวเรา)
        if event.widget is self:
            self.theme.unsubscribe(self.apply_theme)
