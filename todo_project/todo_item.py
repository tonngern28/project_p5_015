"""
ไฟล์: todo_item.py
คอมโพเนนต์ TodoItem — แสดงงาน 1 ชิ้น พร้อมช่องติ๊กและปุ่มลบ
"""
import tkinter as tk
from tkinter import font as tkfont  # ใช้ตั้งค่าฟอนต์ โดยเฉพาะตัวขีดฆ่า (overstrike)


class TodoItem(tk.Frame):
    """
    แสดงงานเพียงชิ้นเดียว ประกอบด้วย ช่องติ๊ก + ข้อความงาน + ปุ่มลบ
    คลาสนี้ "ไม่เก็บ state" ของ todos เลย เพียงรับข้อมูลมาแสดงผล
    และเรียก callback เมื่อผู้ใช้กดติ๊กหรือกดลบ
    """

    def __init__(self, parent, todo, on_toggle, on_delete):
        """
        parent    : widget แม่ (กล่องรายการงาน)
        todo      : dict ของงานนี้ เช่น {"id": 123, "text": "ทำการบ้านคณิต", "done": False}
        on_toggle : callback เรียกเมื่อติ๊กเสร็จ/ยกเลิก (ส่ง id ของงานกลับไป)
        on_delete : callback เรียกเมื่อกดลบ (ส่ง id ของงานกลับไป)
        """
        super().__init__(parent, bg="white")

        # อ่านสถานะว่างานนี้เสร็จแล้วหรือยัง (True/False)
        done = todo["done"]

        # BooleanVar เก็บค่า True/False ของช่องติ๊ก ตั้งค่าเริ่มต้นตามสถานะของงาน
        self.done_var = tk.BooleanVar(value=done)

        # สร้างช่องติ๊ก (Checkbutton)
        #   variable=self.done_var -> แสดงเครื่องหมายถูกตาม done_var
        #   command=lambda: ...    -> เมื่อคลิก ให้เรียก on_toggle พร้อมส่ง id ของงานนี้
        tk.Checkbutton(
            self,
            variable=self.done_var,
            bg="white",
            command=lambda: on_toggle(todo["id"]),
        ).pack(side="left")

        # overstrike=done -> ถ้าเสร็จแล้ว (True) จะมีเส้นขีดฆ่าทับข้อความ
        text_font = tkfont.Font(family="Tahoma", size=12, overstrike=done)

        # สร้างป้ายข้อความ (Label) แสดงชื่องาน
        #   fg: เสร็จแล้วใช้สีเทาจาง ยังไม่เสร็จใช้สีเข้ม
        #   anchor="w": จัดข้อความชิดซ้าย (w = west)
        tk.Label(
            self,
            text=todo["text"],
            font=text_font,
            bg="white",
            anchor="w",
            fg="#9ca3af" if done else "#1f2937",
        ).pack(side="left", fill="x", expand=True)

        # สร้างปุ่ม "ลบ" วางชิดขวา เมื่อคลิกให้เรียก on_delete พร้อมส่ง id
        tk.Button(
            self,
            text="ลบ",
            bg="#fee2e2",
            fg="#b91c1c",
            relief="flat",
            command=lambda: on_delete(todo["id"]),
        ).pack(side="right")
