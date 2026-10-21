# ============================================================
# quote_widget.py (Bonus) แสดงคำคม พิสูจน์ว่า Card ใส่เนื้อหาอะไรก็ได้
# ============================================================
import tkinter as tk
from card import Card


class QuoteWidget(Card):
    def __init__(self, parent):
        super().__init__(parent, title="💬 คำคมวันนี้")
        tk.Label(self.body, text="ทุกความสำเร็จเริ่มจากการลงมือทำ",
                 font=("Helvetica", 11, "italic"), wraplength=180, justify="left").pack(anchor="w")
        self.apply_theme(self.theme.theme)
