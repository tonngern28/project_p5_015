"""
ไฟล์: app.py
คอมโพเนนต์ App — เก็บ state ทั้งหมด (Lift State Up)
แอปเตือนความจำการบ้านก่อนสอบกลางภาค แยกตามรายวิชา
"""
import json
import os
import time
import tkinter as tk
from tkinter import ttk

from todo_input import TodoInput
from todo_item import TodoItem

SAVE_FILE = "todos.json"
ALL_SUBJECTS = "ทุกวิชา"  # ค่าพิเศษของตัวกรองวิชา หมายถึงไม่กรอง


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("เตือนความจำการบ้าน")
        self.geometry("520x640")
        self.configure(bg="white")

        # ---------- STATE (อยู่ที่ App ที่เดียว) ----------
        self.todos = self.load()               # รายการการบ้านทั้งหมด
        self.filter = "all"                    # ตัวกรองสถานะ: all / active / done
        self.subject_filter = ALL_SUBJECTS     # ตัวกรองวิชา

        # ---------- หัวข้อ ----------
        tk.Label(
            self, text="การบ้านก่อนสอบกลางภาค", font=("Tahoma", 18, "bold"),
            bg="white", fg="#312e81",
        ).pack(pady=(16, 2))
        tk.Label(
            self, text="ติ๊กเมื่อทำเสร็จ ลบเมื่อไม่ต้องทำแล้ว", font=("Tahoma", 10),
            bg="white", fg="#6b7280",
        ).pack(pady=(0, 10))

        # ---------- ช่องกรอก (ส่ง callback ลงไป) ----------
        TodoInput(self, on_add=self.add_todo).pack(fill="x", padx=16)

        # ---------- แถบตัวกรอง ----------
        bar = tk.Frame(self, bg="white")
        bar.pack(fill="x", padx=16, pady=10)

        # ปุ่มกรองตามสถานะ
        for key, label in [("all", "ทั้งหมด"), ("active", "ยังไม่เสร็จ"), ("done", "เสร็จแล้ว")]:
            tk.Button(
                bar, text=label, relief="groove",
                command=lambda k=key: self.set_filter(k),
            ).pack(side="left", padx=(0, 6))

        # Combobox กรองตามวิชา (อ่านอย่างเดียว) รายการวิชาจะอัปเดตใน render()
        self.subject_var = tk.StringVar(value=ALL_SUBJECTS)
        self.subject_box = ttk.Combobox(
            bar, textvariable=self.subject_var, state="readonly", width=14,
            values=[ALL_SUBJECTS],
        )
        self.subject_box.pack(side="right")
        self.subject_box.bind("<<ComboboxSelected>>", lambda e: self.set_subject_filter())

        # ---------- รายการงาน ----------
        self.list_frame = tk.Frame(self, bg="white")
        self.list_frame.pack(fill="both", expand=True, padx=16)

        # ---------- สรุปด้านล่าง ----------
        self.count_label = tk.Label(self, bg="white", fg="#1f2937", font=("Tahoma", 12, "bold"))
        self.count_label.pack(pady=(8, 0))
        self.summary_label = tk.Label(self, bg="white", fg="#6b7280", font=("Tahoma", 10),
                                      wraplength=480, justify="center")
        self.summary_label.pack(pady=(2, 4))

        tk.Button(
            self, text="ล้างงานที่เสร็จแล้ว", relief="flat", bg="#f3f4f6",
            command=self.clear_done,
        ).pack(pady=(0, 14))

        self.render()

    # -----------------------------------------------------------
    # ฟังก์ชันแก้ไข state (callbacks)
    # -----------------------------------------------------------
    def add_todo(self, subject, text):
        """เพิ่มการบ้านใหม่ พร้อมวิชา (เรียกจาก TodoInput)"""
        self.todos.append({
            "id": int(time.time() * 1000),  # เลข unique จากเวลา
            "subject": subject,             # วิชา
            "text": text,                   # รายละเอียดการบ้าน
            "done": False,
        })
        self.update_ui()

    def toggle_todo(self, todo_id):
        """สลับเสร็จ/ยังไม่เสร็จ (เรียกจาก TodoItem)"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["done"] = not todo["done"]
        self.update_ui()

    def delete_todo(self, todo_id):
        """ลบงานออก (เรียกจาก TodoItem)"""
        self.todos = [t for t in self.todos if t["id"] != todo_id]
        self.update_ui()

    def clear_done(self):
        """ลบงานที่ติ๊กเสร็จแล้วทั้งหมดในครั้งเดียว"""
        self.todos = [t for t in self.todos if not t["done"]]
        self.update_ui()

    def set_filter(self, key):
        self.filter = key
        self.render()

    def set_subject_filter(self):
        self.subject_filter = self.subject_var.get()
        self.render()

    # -----------------------------------------------------------
    # helpers
    # -----------------------------------------------------------
    def update_ui(self):
        self.save()
        self.render()

    def render(self):
        """วาดหน้าจอใหม่ตาม state ปัจจุบัน"""
        # 1) อัปเดตรายการวิชาใน Combobox จากวิชาที่มีงานอยู่จริง (ไม่ซ้ำ รักษาลำดับ)
        subjects = list(dict.fromkeys(t["subject"] for t in self.todos))
        self.subject_box.config(values=[ALL_SUBJECTS] + subjects)
        # ถ้าวิชาที่เลือกกรองอยู่ไม่มีงานเหลือแล้ว ให้กลับไปดูทุกวิชา
        if self.subject_filter != ALL_SUBJECTS and self.subject_filter not in subjects:
            self.subject_filter = ALL_SUBJECTS
        self.subject_var.set(self.subject_filter)

        # 2) ล้างรายการเก่า
        for child in self.list_frame.winfo_children():
            child.destroy()

        # 3) กรองตามสถานะ และตามวิชา
        visible = self.todos
        if self.filter == "active":
            visible = [t for t in visible if not t["done"]]
        elif self.filter == "done":
            visible = [t for t in visible if t["done"]]
        if self.subject_filter != ALL_SUBJECTS:
            visible = [t for t in visible if t["subject"] == self.subject_filter]

        # 4) สร้าง TodoItem ส่ง callback ลงไป
        for todo in visible:
            TodoItem(self.list_frame, todo, self.toggle_todo, self.delete_todo).pack(fill="x", pady=3)
        if not visible:
            tk.Label(self.list_frame, text="ยังไม่มีงานในหมวดนี้", bg="white",
                     fg="#9ca3af").pack(pady=16)

        # 5) จำนวนงานที่เหลือทั้งหมด (ไม่ขึ้นกับตัวกรอง)
        pending = [t for t in self.todos if not t["done"]]
        self.count_label.config(text=f"เหลืองานที่ต้องทำอีก {len(pending)} งาน")

        # 6) สรุปงานค้างแยกตามวิชา เช่น "คณิตศาสตร์ 2 | ภาษาไทย 1"
        per_subject = {}
        for t in pending:
            per_subject[t["subject"]] = per_subject.get(t["subject"], 0) + 1
        if per_subject:
            self.summary_label.config(
                text="งานค้างแยกตามวิชา: " + " | ".join(f"{s} {n}" for s, n in per_subject.items())
            )
        elif self.todos:
            self.summary_label.config(text="ทำการบ้านครบทุกวิชาแล้ว เยี่ยมมาก")
        else:
            self.summary_label.config(text="เริ่มจากเลือกวิชา แล้วพิมพ์การบ้านที่ต้องทำด้านบน")

    def save(self):
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.todos, f, ensure_ascii=False, indent=2)

    def load(self):
        """โหลดจากไฟล์ งานเก่าที่ไม่มีฟิลด์ subject จะได้วิชา "อื่น ๆ" """
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, encoding="utf-8") as f:
                    todos = json.load(f)
                for t in todos:
                    t.setdefault("subject", "อื่น ๆ")
                return todos
            except (json.JSONDecodeError, OSError, AttributeError):
                pass
        return []
