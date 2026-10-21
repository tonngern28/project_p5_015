"""
ไฟล์: todo_item.py
คอมโพเนนต์ TodoItem — แสดงการบ้าน 1 ชิ้น: ป้ายวิชา + ข้อความ + ช่องติ๊ก + ปุ่มลบ
"""
import tkinter as tk
from tkinter import font as tkfont

# สีป้ายวิชา (วิชาเดียวกันได้สีเดียวกันเสมอ เพื่อให้สแกนด้วยตาได้เร็ว)
SUBJECT_COLORS = ["#dbeafe", "#dcfce7", "#fef3c7", "#fce7f3", "#ede9fe", "#ffedd5"]


def subject_color(subject):
    """เลือกสีจากชื่อวิชา โดยรวมค่ารหัสตัวอักษรแล้วหารเอาเศษตามจำนวนสี"""
    return SUBJECT_COLORS[sum(ord(c) for c in subject) % len(SUBJECT_COLORS)]


class TodoItem(tk.Frame):
    """ไม่เก็บ state ของ todos รับข้อมูลมาแสดงและเรียก callback เท่านั้น"""

    def __init__(self, parent, todo, on_toggle, on_delete):
        """
        todo : dict {"id": ..., "subject": "คณิตศาสตร์", "text": "...", "done": False}
        """
        super().__init__(parent, bg="white")
        done = todo["done"]

        # ช่องติ๊กเสร็จ/ยังไม่เสร็จ
        self.done_var = tk.BooleanVar(value=done)
        tk.Checkbutton(
            self, variable=self.done_var, bg="white",
            command=lambda: on_toggle(todo["id"]),
        ).pack(side="left")

        # ป้ายชื่อวิชา (badge) ใช้สีตามวิชา; ถ้างานเสร็จแล้วให้สีจางลง
        tk.Label(
            self, text=todo["subject"], font=("Tahoma", 9),
            bg="#f3f4f6" if done else subject_color(todo["subject"]),
            fg="#9ca3af" if done else "#374151", padx=6, pady=1,
        ).pack(side="left", padx=(0, 8))

        # ข้อความการบ้าน: ขีดฆ่าและสีจางเมื่อทำเสร็จแล้ว
        text_font = tkfont.Font(family="Tahoma", size=12, overstrike=done)
        tk.Label(
            self, text=todo["text"], font=text_font, bg="white", anchor="w",
            fg="#9ca3af" if done else "#1f2937",
        ).pack(side="left", fill="x", expand=True)

        # ปุ่มลบงานที่ไม่ต้องทำแล้ว
        tk.Button(
            self, text="ลบ", bg="#fee2e2", fg="#b91c1c", relief="flat",
            command=lambda: on_delete(todo["id"]),
        ).pack(side="right")
