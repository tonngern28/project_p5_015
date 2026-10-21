"""
ไฟล์: todo_input.py
คอมโพเนนต์ TodoInput — เลือกวิชา + พิมพ์รายละเอียดการบ้าน + ปุ่มเพิ่มงาน
"""
import tkinter as tk
from tkinter import ttk  # ttk มี Combobox (ช่องเลือกแบบ drop-down) ให้ใช้

# รายชื่อวิชาเริ่มต้นให้เลือก (ผู้ใช้พิมพ์ชื่อวิชาอื่นเองได้ด้วย)
DEFAULT_SUBJECTS = [
    "คณิตศาสตร์",
    "วิทยาศาสตร์",
    "ภาษาไทย",
    "ภาษาอังกฤษ",
    "สังคมศึกษา",
    "อื่น ๆ",
]


class TodoInput(tk.Frame):
    def __init__(self, parent, on_add):
        """
        parent : widget แม่
        on_add : callback จาก App เรียกเป็น on_add(subject, text)
                 คือส่งทั้ง "วิชา" และ "รายละเอียดการบ้าน" กลับไป
        """
        super().__init__(parent, bg="white")
        self.on_add = on_add

        # state ของช่องกรอกเท่านั้น (ไม่ใช่ todos)
        self.subject_var = tk.StringVar(value=DEFAULT_SUBJECTS[0])
        self.text_var = tk.StringVar()

        # แถวที่ 1: เลือกวิชา
        row1 = tk.Frame(self, bg="white")
        row1.pack(fill="x")
        tk.Label(row1, text="วิชา:", bg="white", font=("Tahoma", 11)).pack(side="left")

        # Combobox แบบพิมพ์เองได้ (ไม่ตั้ง state="readonly")
        # ถ้าวิชาไม่อยู่ในรายการ ก็พิมพ์ชื่อวิชาใหม่ลงไปได้เลย
        ttk.Combobox(
            row1, textvariable=self.subject_var, values=DEFAULT_SUBJECTS, width=22
        ).pack(side="left", padx=(8, 0))

        # แถวที่ 2: พิมพ์การบ้าน + ปุ่มเพิ่ม
        row2 = tk.Frame(self, bg="white")
        row2.pack(fill="x", pady=(8, 0))

        self.entry = tk.Entry(row2, textvariable=self.text_var, font=("Tahoma", 12))
        self.entry.pack(side="left", fill="x", expand=True, ipady=6)
        self.entry.bind("<Return>", lambda e: self.submit())  # กด Enter เพื่อเพิ่ม

        tk.Button(
            row2, text="เพิ่มงาน", font=("Tahoma", 11), bg="#4f46e5", fg="white",
            relief="flat", padx=12, command=self.submit,
        ).pack(side="left", padx=(8, 0))

    def submit(self):
        """ตรวจข้อมูล แล้วส่ง (วิชา, ข้อความ) ให้ App"""
        text = self.text_var.get().strip()
        subject = self.subject_var.get().strip() or "อื่น ๆ"  # ไม่ได้กรอกวิชา -> "อื่น ๆ"

        if not text:  # ไม่ได้พิมพ์การบ้าน -> ไม่เพิ่ม
            return

        self.on_add(subject, text)

        # เคลียร์เฉพาะช่องการบ้าน แต่เก็บวิชาไว้ เพราะมักเพิ่มหลายงานของวิชาเดียวกันต่อเนื่อง
        self.text_var.set("")
        self.entry.focus_set()
