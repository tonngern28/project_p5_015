# ============================================================
# clock_widget.py (Bonus) นาฬิกาที่อัปเดตทุกวินาที ใช้ Card เป็นฐานเหมือนกัน
# ============================================================
import time
import tkinter as tk
from card import Card


class ClockWidget(Card):
    def __init__(self, parent):
        super().__init__(parent, title="🕒 เวลาปัจจุบัน")
        self.time_label = tk.Label(self.body, font=("Helvetica", 24, "bold"))
        self.time_label.pack(anchor="w")
        self._job = None          # เก็บ id ของ timer เพื่อใช้ยกเลิกตอนปิด
        self._tick()              # เริ่มเดินนาฬิกา
        self.apply_theme(self.theme.theme)

    def _tick(self):
        self.time_label.configure(text=time.strftime("%H:%M:%S"))
        # สั่งให้เรียกตัวเองซ้ำทุก 1000 ms (1 วินาที)
        self._job = self.after(1000, self._tick)

    def destroy(self):
        # ยกเลิก timer ก่อนทำลาย ป้องกัน error หลังปิดหน้าต่าง
        if self._job is not None:
            self.after_cancel(self._job)
        super().destroy()
