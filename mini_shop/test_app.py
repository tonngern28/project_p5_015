"""
test_app.py : ทดสอบตามเกณฑ์การผ่านโดยไม่ต้องต่อเน็ต (จำลอง API)
รัน:  python test_app.py
"""
import api
from app import app

FAKE = [
    {"id": 1, "title": "Backpack", "price": 100.0, "image": "x.png", "category": "bag", "description": "d"},
    {"id": 2, "title": "T-Shirt", "price": 20.0, "image": "y.png", "category": "cloth", "description": "d"},
]
api.fetch_products = lambda limit=8: FAKE
api.fetch_product = lambda pid: next(p for p in FAKE if p["id"] == pid)

c = app.test_client()

assert "Backpack" in c.get("/").get_data(as_text=True)          # ดึงสินค้าได้
c.post("/cart/add/1"); c.post("/cart/add/1"); c.post("/cart/add/2")
html = c.get("/").get_data(as_text=True)
assert '<span class="badge">3</span>' in html                    # Navbar อัปเดต
cart = c.get("/cart").get_data(as_text=True)
assert "Backpack" in cart and "T-Shirt" in cart                  # เห็นสินค้าใน /cart
assert "฿7,000.00" in cart and "฿700.00" in cart                 # 100*35*2 และ 20*35
assert "฿7,700.00" in cart                                       # ราคารวม
c.post("/cart/decrease/2")                                       # ลดจนหมด -> หาย
assert "T-Shirt" not in c.get("/cart").get_data(as_text=True)
c.post("/cart/remove/1")                                         # ลบสินค้า
assert "ตะกร้าว่างเปล่า" in c.get("/cart").get_data(as_text=True)
assert c.get("/product/1").status_code == 200                    # หน้ารายละเอียด
print("ผ่านทุกการทดสอบ")
