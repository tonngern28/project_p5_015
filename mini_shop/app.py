"""
app.py
======
จุดเริ่มต้นของแอป Mini Shop (Flask)

แมปแนวคิดจาก React -> Flask:
  React Router  /  /cart  /product/:id   ->  @app.route(...)
  CartContext Provider                    ->  context_processor (ฉีดข้อมูลให้ทุกเทมเพลต)
  Navbar / ProductCard                    ->  templates/base.html, templates/_macros.html
  ShopPage / CartPage                     ->  templates/shop.html, templates/cart.html
  Lazy Loading (Cart)                     ->  import โมดูลตะกร้าเมื่อถูกเรียกครั้งแรก + <img loading="lazy">
"""

import os

from flask import Flask, flash, redirect, render_template, request, url_for

import api
from cart_context import to_thb, use_cart

app = Flask(__name__)
# ใช้เซ็นรหัสคุกกี้ session (ของจริงควรตั้งผ่าน environment variable)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")


# ----------------------------------------------------------------------
# "Provider": ฉีดตะกร้าให้ "ทุกเทมเพลต" โดยอัตโนมัติ
# ทำให้ Navbar (ใน base.html) เห็นจำนวนสินค้าได้ทุกหน้า โดยไม่ต้องส่งค่าเองใน route
# ----------------------------------------------------------------------
@app.context_processor
def inject_cart():
    cart = use_cart()
    return {"cart_ctx": cart, "to_thb": to_thb}


def _back(default_endpoint: str = "shop_page"):
    """กลับไปหน้าเดิมที่ผู้ใช้กดมา (ถ้าไม่มี referrer ให้ไปหน้าเริ่มต้น)"""
    return redirect(request.referrer or url_for(default_endpoint))


# ----------------------------------------------------------------------
# หน้า "/" : ShopPage
# ----------------------------------------------------------------------
@app.route("/")
def shop_page():
    products, error = [], None
    try:
        products = api.fetch_products(limit=8)  # ดึงจาก API จริง
    except api.ApiError as e:
        error = str(e)  # แสดงข้อความผิดพลาดแทนที่จะให้แอปพัง
    return render_template("shop.html", products=products, error=error)


# ----------------------------------------------------------------------
# หน้า "/cart" : CartPage
# (Bonus) Lazy Loading: ย้ายตรรกะหน้าตะกร้าไปโหลดตอนถูกเรียกครั้งแรกเท่านั้น
# ----------------------------------------------------------------------
@app.route("/cart")
def cart_page():
    from pages.cart_view import render_cart  # lazy import (เหมือน React.lazy)
    return render_cart()


# ----------------------------------------------------------------------
# (Bonus) หน้า "/product/<id>" : รายละเอียดสินค้า
# ----------------------------------------------------------------------
@app.route("/product/<int:product_id>")
def product_page(product_id):
    try:
        product = api.fetch_product(product_id)
    except api.ApiError as e:
        return render_template("product.html", product=None, error=str(e)), 502
    return render_template("product.html", product=product, error=None)


# ----------------------------------------------------------------------
# Actions ของตะกร้า (ใช้ POST เพราะเป็นการเปลี่ยนแปลงข้อมูล)
# ----------------------------------------------------------------------
@app.post("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    try:
        product = api.fetch_product(product_id)
        use_cart().add_to_cart(product)
        flash(f"เพิ่ม “{product['title'][:30]}” ลงตะกร้าแล้ว")
    except api.ApiError as e:
        flash(str(e))
    return _back()


@app.post("/cart/remove/<int:product_id>")
def remove_from_cart(product_id):
    use_cart().remove_from_cart(product_id)
    return _back("cart_page")


@app.post("/cart/increase/<int:product_id>")
def increase(product_id):
    use_cart().increase(product_id)
    return _back("cart_page")


@app.post("/cart/decrease/<int:product_id>")
def decrease(product_id):
    use_cart().decrease(product_id)
    return _back("cart_page")


@app.post("/cart/checkout")
def checkout():
    cart = use_cart()
    if cart.total_items == 0:
        flash("ตะกร้าว่างเปล่า")
    else:
        flash(f"สั่งซื้อสำเร็จ! ยอดรวม ฿{cart.total_price:,.2f}")
        cart.clear()
    return redirect(url_for("cart_page"))


if __name__ == "__main__":
    app.run(debug=True)
