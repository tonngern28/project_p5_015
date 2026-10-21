"""
pages/cart_view.py
==================
ตรรกะของหน้าตะกร้า (CartPage) แยกเป็นโมดูลต่างหาก
app.py จะ import ไฟล์นี้เมื่อมีคนเปิด /cart ครั้งแรกเท่านั้น (Lazy Loading)
"""

from flask import render_template

from cart_context import use_cart


def render_cart():
    cart = use_cart()  # ดึงตะกร้ากลางด้วย useCart() เทียบเท่า
    return render_template("cart.html", items=cart.cart)
