"""
ไฟล์: todo_input.py
คอมโพเนนต์ TodoInput — ช่องพิมพ์และปุ่มเพิ่มงาน
"""
import tkinter as tk  # ไลบรารีสร้างหน้าต่างโปรแกรม (GUI) ที่มากับ Python


class TodoInput(tk.Frame):
    """
    tk.Frame คือ "กล่อง" สำหรับจัดกลุ่ม widget ไว้ด้วยกัน
    เราสืบทอด (inherit) จาก tk.Frame เพื่อให้คลาสนี้เป็นกล่องที่ใส่ช่องพิมพ์กับปุ่มไว้ข้างใน
    """

    def __init__(self, parent, on_add):
        """
        parent : widget แม่ที่จะนำกล่องนี้ไปวางข้างใน
        on_add : callback function ที่ App ส่งเข้ามา
                 เมื่อผู้ใช้กดเพิ่มงาน เราจะเรียก on_add(ข้อความ) เพื่อบอกให้ App เพิ่มงาน
        """
        # เรียก __init__ ของ tk.Frame ก่อนเสมอ เพื่อสร้างกล่องให้เรียบร้อย
        super().__init__(parent, bg="white")

        # เก็บ callback ไว้ในตัวแปรของออบเจ็กต์ เพื่อเรียกใช้ทีหลังในเมธอด submit
        self.on_add = on_add

        # StringVar คือตัวแปรพิเศษของ tkinter ที่ผูกกับช่องพิมพ์
        # หมายเหตุ: นี่คือ state ของ "ข้อความที่กำลังพิมพ์" เท่านั้น ไม่ใช่ state ของ todos
        self.text_var = tk.StringVar()

        # สร้างช่องพิมพ์ (Entry) และผูกกับ text_var
        self.entry = tk.Entry(self, textvariable=self.text_var, font=("Tahoma", 12))

        # pack() คือการวาง widget ลงในกล่อง
        #   side="left"  -> วางชิดซ้าย
        #   fill="x"     -> ขยายเต็มความกว้าง
        #   expand=True  -> ใช้พื้นที่ว่างที่เหลือ (ช่องพิมพ์จะยืดตามหน้าต่าง)
        #   ipady=6      -> เพิ่มความสูงภายในช่องพิมพ์
        self.entry.pack(side="left", fill="x", expand=True, ipady=6)

        # bind() ผูก "เหตุการณ์" เข้ากับฟังก์ชัน
        # <Return> คือการกดปุ่ม Enter -> ให้เรียก self.submit()
        # lambda e: ... ใช้เพราะ tkinter ส่งข้อมูลเหตุการณ์ (e) มาให้ แต่เราไม่ได้ใช้
        self.entry.bind("<Return>", lambda e: self.submit())

        # สร้างปุ่ม "เพิ่มงาน" เมื่อคลิกให้เรียก self.submit()
        tk.Button(
            self,
            text="เพิ่มงาน",
            font=("Tahoma", 11),
            bg="#4f46e5",
            fg="white",
            relief="flat",
            padx=12,
            command=self.submit,
        ).pack(side="left", padx=(8, 0))  # เว้นระยะซ้าย 8 พิกเซล ขวา 0

    def submit(self):
        """ทำงานเมื่อกด Enter หรือคลิกปุ่ม: ตรวจข้อความ แล้วส่งให้ App"""
        # ดึงข้อความจากช่องพิมพ์ และตัดช่องว่างหน้า-หลังออก
        text = self.text_var.get().strip()

        # ถ้าไม่ได้พิมพ์อะไรเลย ให้หยุด ไม่เพิ่มงานว่าง
        if not text:
            return

        # เรียก callback ที่ App ส่งมา เพื่อให้ App เพิ่มงานลงใน todos
        self.on_add(text)

        # เคลียร์ช่องพิมพ์ให้ว่าง พร้อมพิมพ์งานถัดไป
        self.text_var.set("")
