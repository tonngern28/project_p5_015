"""
cart_context.py
===============
เทียบเท่า CartContext + useCart() ใน React

แนวคิด:
  - React: Context ทำให้ "ทุกคอมโพเนนต์" เข้าถึงตะกร้าเดียวกันได้ ไม่ว่าอยู่หน้าไหน
  - Flask: เราเก็บตะกร้าไว้ใน `session` (คุกกี้ที่เซ็นรหัสแล้ว) ซึ่งเป็น "แหล่งข้อมูลกลาง"
    เดียวของผู้ใช้แต่ละคน แล้วห่อด้วยคลาส CartContext เพื่อให้ทุกหน้า/ทุกเทมเพลต
    (Navbar, ShopPage, CartPage) ใช้ผ่านฟังก์ชัน use_cart() ตัวเดียวกัน

  *** ข้อห้ามตามโจทย์: ห้ามเก็บตะกร้าไว้ในตัวแปรของ Navbar หรือ ShopPage ***
  เราจึงไม่เก็บตะกร้าใน route/เทมเพลตใด ๆ เลย เก็บที่นี่ที่เดียว
"""

from flask import g, session

# อัตราแลกเปลี่ยนตามโจทย์: USD -> THB คูณ 35
USD_TO_THB = 35


def to_thb(price_usd: float) -> float:
    """แปลงราคา USD เป็น THB (คูณ 35) ปัดทศนิยม 2 ตำแหน่ง"""
    return round(float(price_usd) * USD_TO_THB, 2)


class CartContext:
    """
    ตัวจัดการตะกร้าสินค้า (เทียบเท่า CartProvider)

    โครงสร้างของแต่ละรายการใน cart (dict):
        {
          "id": 1,
          "title": "ชื่อสินค้า",
          "price": 3500.0,     # ราคาเป็นบาท (แปลงแล้ว)
          "image": "https://...",
          "quantity": 2
        }
    """

    SESSION_KEY = "cart"

    def __init__(self, flask_session):
        # เก็บ reference ของ session ไว้ เพื่ออ่าน/เขียนตะกร้า
        self._session = flask_session

    # ------------------------------------------------------------------
    # state: cart
    # ------------------------------------------------------------------
    @property
    def cart(self) -> list:
        """รายการสินค้าในตะกร้า (เทียบเท่า state `cart`)"""
        return self._session.get(self.SESSION_KEY, [])

    def _save(self, cart: list) -> None:
        """บันทึกตะกร้ากลับลง session (ต้องเรียกทุกครั้งที่แก้ไข)"""
        self._session[self.SESSION_KEY] = cart
        # บอก Flask ว่า session ถูกแก้ไขแล้ว (เพราะเราแก้ list ซ้อนใน session)
        self._session.modified = True

    # ------------------------------------------------------------------
    # actions
    # ------------------------------------------------------------------
    def add_to_cart(self, product: dict) -> None:
        """
        เพิ่มสินค้า: ถ้ามีอยู่แล้วให้ +1 quantity, ถ้ายังไม่มีให้เพิ่มรายการใหม่
        product ที่รับเข้ามาเป็นข้อมูลดิบจาก API (ราคาเป็น USD)
        """
        cart = list(self.cart)  # คัดลอกก่อนแก้ไข (ไม่แก้ของเดิมตรง ๆ)
        for item in cart:
            if item["id"] == product["id"]:
                item["quantity"] += 1  # มีอยู่แล้ว -> เพิ่มจำนวน
                self._save(cart)
                return
        # ยังไม่มี -> เพิ่มรายการใหม่ พร้อมแปลงราคาเป็นบาท
        cart.append({
            "id": product["id"],
            "title": product["title"],
            "price": to_thb(product["price"]),
            "image": product["image"],
            "quantity": 1,
        })
        self._save(cart)

    def remove_from_cart(self, product_id: int) -> None:
        """ลบสินค้าออกจากตะกร้าทั้งรายการ (ตาม id)"""
        self._save([i for i in self.cart if i["id"] != product_id])

    def increase(self, product_id: int) -> None:
        """(Bonus) เพิ่มจำนวนสินค้า 1 ชิ้น"""
        cart = list(self.cart)
        for item in cart:
            if item["id"] == product_id:
                item["quantity"] += 1
        self._save(cart)

    def decrease(self, product_id: int) -> None:
        """(Bonus) ลดจำนวนสินค้า 1 ชิ้น ถ้าเหลือ 0 ให้ลบออกจากตะกร้า"""
        cart = list(self.cart)
        for item in cart:
            if item["id"] == product_id:
                item["quantity"] -= 1
        # กรองรายการที่จำนวนเหลือ 0 ทิ้ง
        self._save([i for i in cart if i["quantity"] > 0])

    def clear(self) -> None:
        """ล้างตะกร้า (ใช้หลังกดสั่งซื้อ)"""
        self._save([])

    # ------------------------------------------------------------------
    # derived values (ค่าที่คำนวณจาก cart)
    # ------------------------------------------------------------------
    @property
    def total_items(self) -> int:
        """จำนวนชิ้นรวมทั้งหมด (รวม quantity ของทุกรายการ)"""
        return sum(i["quantity"] for i in self.cart)

    @property
    def total_price(self) -> float:
        """ราคารวมเป็นบาท = ผลรวมของ (ราคา x จำนวน)"""
        return round(sum(i["price"] * i["quantity"] for i in self.cart), 2)


def use_cart() -> CartContext:
    """
    เทียบเท่า useCart() hook
    เรียกจากที่ใดก็ได้ในแอป จะได้ตัวจัดการตะกร้าตัวเดียวกันภายใน request นั้น
    ใช้ flask.g เพื่อสร้างแค่ครั้งเดียวต่อ request
    """
    if "cart_ctx" not in g:
        g.cart_ctx = CartContext(session)
    return g.cart_ctx
