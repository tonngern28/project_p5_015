"""
ไฟล์: app.py
คอมโพเนนต์ App — คอมโพเนนต์แม่ที่เก็บ state ทั้งหมด (Lift State Up)
"""
import json   # แปลงข้อมูล list/dict <-> ข้อความ JSON เพื่อบันทึกลงไฟล์
import os     # ตรวจว่าไฟล์บันทึกมีอยู่แล้วหรือไม่
import time   # สร้างเลข id ไม่ซ้ำ (เทียบเท่า Date.now() ของ JavaScript)
import tkinter as tk

# ดึงคอมโพเนนต์ลูกจากไฟล์อื่นมาใช้
# รูปแบบ: from ชื่อไฟล์ (ไม่ต้องใส่ .py) import ชื่อคลาส
from todo_input import TodoInput
from todo_item import TodoItem

# ชื่อไฟล์ที่ใช้เก็บข้อมูล (Bonus: เทียบเท่า localStorage ของเว็บ)
SAVE_FILE = "todos.json"


class App(tk.Tk):
    """
    tk.Tk คือหน้าต่างหลักของโปรแกรม App ทำหน้าที่:
      1) เก็บ state (todos และ filter)
      2) มีฟังก์ชันแก้ไข state (add_todo, toggle_todo, delete_todo)
      3) ประกอบ TodoInput และ TodoItem เข้าด้วยกัน พร้อมส่ง callback ลงไป
    """

    def __init__(self):
        super().__init__()  # สร้างหน้าต่างหลัก

        # ---------- ตั้งค่าหน้าต่าง ----------
        self.title("รายการสิ่งที่ต้องทำ")
        self.geometry("460x560")
        self.configure(bg="white")

        # ---------- STATE (เก็บไว้ที่ App ที่เดียว) ----------
        # รายการงานทั้งหมด: โหลดจากไฟล์ ถ้าไม่มีไฟล์จะได้ list ว่าง []
        self.todos = self.load()

        # ตัวกรอง: "all" (ทั้งหมด), "active" (ยังไม่เสร็จ), "done" (เสร็จแล้ว)
        self.filter = "all"

        # ---------- ส่วนหัวข้อ ----------
        tk.Label(
            self,
            text="รายการสิ่งที่ต้องทำ",
            font=("Tahoma", 18, "bold"),
            bg="white",
            fg="#312e81",
        ).pack(pady=(16, 8))

        # ---------- ช่องพิมพ์ ----------
        # ส่ง self.add_todo ลงไปเป็น on_add (นี่คือการ "ส่ง callback ลงไป")
        # ส่งชื่อฟังก์ชันโดยไม่ใส่วงเล็บ () เพราะต้องการส่งตัวฟังก์ชัน ไม่ใช่เรียกใช้ทันที
        TodoInput(self, on_add=self.add_todo).pack(fill="x", padx=16)

        # ---------- แถบปุ่มกรอง (Bonus) ----------
        bar = tk.Frame(self, bg="white")
        bar.pack(fill="x", padx=16, pady=10)

        for key, label in [("all", "ทั้งหมด"), ("active", "ยังไม่เสร็จ"), ("done", "เสร็จแล้ว")]:
            tk.Button(
                bar,
                text=label,
                relief="groove",
                # k=key คือ "default argument" เพื่อจับค่า key ของรอบนั้นไว้
                # ถ้าไม่ใส่ ทุกปุ่มจะใช้ key ตัวสุดท้ายของลูป
                command=lambda k=key: self.set_filter(k),
            ).pack(side="left", padx=(0, 6))

        # ---------- กล่องแสดงรายการงาน ----------
        # จะถูกล้างแล้วสร้างใหม่ทุกครั้งที่ state เปลี่ยน (ดูเมธอด render)
        self.list_frame = tk.Frame(self, bg="white")
        self.list_frame.pack(fill="both", expand=True, padx=16)

        # ---------- ป้ายแสดงจำนวนงานที่เหลือ ----------
        self.count_label = tk.Label(self, bg="white", fg="#4b5563", font=("Tahoma", 11))
        self.count_label.pack(pady=12)

        # วาดหน้าจอครั้งแรก เพื่อแสดงงานที่โหลดมาจากไฟล์ (ถ้ามี)
        self.render()

    # -----------------------------------------------------------
    # ฟังก์ชันแก้ไข state (callbacks ที่ส่งลงไปให้ลูก)
    # -----------------------------------------------------------
    def add_todo(self, text):
        """เพิ่มงานใหม่ (ถูกเรียกจาก TodoInput ผ่าน on_add)"""
        new_todo = {
            "id": int(time.time() * 1000),  # เวลาปัจจุบันเป็นมิลลิวินาที = เลขไม่ซ้ำ
            "text": text,                   # ชื่องาน
            "done": False,                  # งานใหม่ยังไม่เสร็จ
        }
        self.todos.append(new_todo)
        self.update_ui()

    def toggle_todo(self, todo_id):
        """สลับสถานะเสร็จ/ยังไม่เสร็จ (ถูกเรียกจาก TodoItem ผ่าน on_toggle)"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["done"] = not todo["done"]  # สลับ True <-> False
        self.update_ui()

    def delete_todo(self, todo_id):
        """ลบงานออก (ถูกเรียกจาก TodoItem ผ่าน on_delete)"""
        # เก็บเฉพาะงานที่ id "ไม่ตรง" กับงานที่จะลบ
        self.todos = [todo for todo in self.todos if todo["id"] != todo_id]
        self.update_ui()

    def set_filter(self, key):
        """เปลี่ยนตัวกรอง แล้ววาดหน้าจอใหม่ (ไม่ได้แก้ข้อมูล จึงไม่ต้องบันทึกไฟล์)"""
        self.filter = key
        self.render()

    # -----------------------------------------------------------
    # ฟังก์ชันช่วยทำงาน (helpers)
    # -----------------------------------------------------------
    def update_ui(self):
        """เรียกทุกครั้งที่ข้อมูล todos เปลี่ยน: บันทึกลงไฟล์ แล้ววาดหน้าจอใหม่"""
        self.save()
        self.render()

    def render(self):
        """วาดรายการงานและจำนวนที่เหลือใหม่ทั้งหมดตาม state ปัจจุบัน"""
        # 1) ล้างรายการเก่าออกจากหน้าจอ
        for child in self.list_frame.winfo_children():
            child.destroy()

        # 2) เลือกงานที่จะแสดงตามตัวกรอง
        if self.filter == "active":
            visible = [t for t in self.todos if not t["done"]]
        elif self.filter == "done":
            visible = [t for t in self.todos if t["done"]]
        else:
            visible = self.todos

        # 3) สร้าง TodoItem ให้งานแต่ละชิ้น พร้อมส่ง callback ลงไป
        for todo in visible:
            TodoItem(
                self.list_frame, todo, self.toggle_todo, self.delete_todo
            ).pack(fill="x", pady=2)

        # 4) ถ้าไม่มีงานให้แสดง ให้ขึ้นข้อความแจ้งแทน
        if not visible:
            tk.Label(
                self.list_frame,
                text="ยังไม่มีงานที่ทำเสร็จแล้ว",
                bg="white",
                fg="#9ca3af",
            ).pack(pady=16)

        # 5) นับจำนวนงานที่ "ยังไม่เสร็จ" จากงานทั้งหมด (ไม่ขึ้นกับตัวกรอง)
        remaining = sum(1 for t in self.todos if not t["done"])
        self.count_label.config(text=f"เหลืองานที่ต้องทำอีก {remaining} งาน")

    def save(self):
        """บันทึกรายการงานทั้งหมดลงไฟล์ JSON (Bonus)"""
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            # ensure_ascii=False -> เก็บภาษาไทยเป็นตัวอักษรจริง, indent=2 -> อ่านไฟล์ง่าย
            json.dump(self.todos, f, ensure_ascii=False, indent=2)

    def load(self):
        """โหลดรายการงานจากไฟล์ JSON ถ้าไม่มีหรืออ่านไม่ได้ให้คืนค่า list ว่าง"""
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass  # ไฟล์เสียหรืออ่านไม่ได้ -> เริ่มด้วยรายการว่าง
        return []
