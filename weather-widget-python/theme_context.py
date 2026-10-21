# ============================================================
# theme_context.py
# หน้าที่: เป็น "ที่เก็บกลาง" ของค่า theme และฟังก์ชัน toggle_theme
# (เทียบเท่า ThemeContext.jsx ในฝั่ง React)
#
# แนวคิด: ใน React คอมโพเนนต์จะ re-render เองเมื่อ Context เปลี่ยน
# ใน Python เราใช้ "Observer Pattern" แทน คือ
#   - คอมโพเนนต์ที่อยากรู้ว่าธีมเปลี่ยน เรียก subscribe(callback) ไว้
#   - เมื่อ toggle_theme() ถูกเรียก ระบบจะเรียก callback ของทุกคนพร้อมกัน
# ผลลัพธ์: ทุกคอมโพเนนต์เปลี่ยนสีพร้อมกัน โดยไม่ต้องส่ง theme ผ่านพารามิเตอร์ต่อกันเป็นทอดๆ
# ============================================================
import json
import os

# ไฟล์สำหรับบันทึกธีม (Bonus: เทียบเท่า localStorage ของเว็บ)
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme_settings.json")

# ชุดสีของแต่ละธีม เก็บเป็นข้อมูลไว้ที่เดียว แก้สีได้ง่าย
PALETTE = {
    "light": {"page_bg": "#f3f4f6", "card_bg": "#ffffff", "text": "#1f2937", "border": "#e5e7eb"},
    "dark": {"page_bg": "#111827", "card_bg": "#1f2937", "text": "#f9fafb", "border": "#374151"},
}


class ThemeProvider:
    """ตัวเก็บสถานะ theme + รายชื่อผู้ที่ subscribe (เทียบเท่า <ThemeProvider> ใน React)"""

    def __init__(self):
        self._listeners = []                 # รายการ callback ของคอมโพเนนต์ที่รอฟังการเปลี่ยนธีม
        self.theme = self._load_theme()      # 'light' หรือ 'dark'
        set_active_provider(self)            # ลงทะเบียนตัวเองเป็น Provider ที่ใช้งานอยู่

    # ---------- การอ่าน/เขียนไฟล์ (Bonus) ----------
    def _load_theme(self):
        """อ่านธีมที่เคยบันทึกไว้ ถ้าไม่มีหรืออ่านไม่ได้ให้ใช้ 'light'"""
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f).get("theme")
            return "dark" if saved == "dark" else "light"
        except (OSError, ValueError):
            return "light"

    def _save_theme(self):
        """บันทึกธีมลงไฟล์ ถ้าบันทึกไม่ได้ก็ปล่อยผ่าน แอปยังใช้งานต่อได้"""
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump({"theme": self.theme}, f)
        except OSError:
            pass

    # ---------- ส่วนของ Observer ----------
    def subscribe(self, callback):
        """ลงทะเบียน callback และเรียกใช้ทันที 1 ครั้งเพื่อให้สีเริ่มต้นถูกต้อง"""
        self._listeners.append(callback)
        callback(self.theme)

    def unsubscribe(self, callback):
        """ยกเลิกการติดตาม (เรียกตอนคอมโพเนนต์ถูกทำลาย)"""
        if callback in self._listeners:
            self._listeners.remove(callback)

    def toggle_theme(self):
        """สลับ light <-> dark แล้วแจ้งทุกคอมโพเนนต์ให้เปลี่ยนสีพร้อมกัน"""
        self.theme = "dark" if self.theme == "light" else "light"
        self._save_theme()
        # ใช้ list(...) คัดลอกก่อนวน เผื่อมีการ unsubscribe ระหว่างวนลูป
        for callback in list(self._listeners):
            callback(self.theme)

    def colors(self):
        """คืนชุดสีของธีมปัจจุบัน"""
        return PALETTE[self.theme]


# ---------- ส่วนของ "Context" ระดับโมดูล ----------
_active_provider = None


def set_active_provider(provider):
    global _active_provider
    _active_provider = provider


def use_theme():
    """Custom hook (เทียบเท่า useTheme()) : ให้คอมโพเนนต์ไหนก็ได้ดึง Provider ได้ตรงๆ"""
    if _active_provider is None:
        raise RuntimeError("use_theme() ต้องถูกเรียกหลังสร้าง ThemeProvider() แล้วเท่านั้น")
    return _active_provider
