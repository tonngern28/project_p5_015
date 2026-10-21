# Mini Shop (Python / Flask)

ร้านค้าออนไลน์จิ๋ว ดึงสินค้าจาก https://fakestoreapi.com/products?limit=8

## วิธีรัน
    python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    python app.py          # เปิด http://127.0.0.1:5000
    python test_app.py     # ทดสอบ (ไม่ต้องใช้เน็ต)

## โครงสร้าง (เทียบกับ React)
| React                     | ไฟล์นี้                                        |
|---------------------------|------------------------------------------------|
| React Router `/`, `/cart` | `app.py` (`@app.route`)                        |
| CartContext + useCart()   | `cart_context.py` (`CartContext`, `use_cart`)  |
| Navbar                    | `templates/base.html`                          |
| ProductCard               | `templates/_macros.html`                       |
| ShopPage / CartPage       | `templates/shop.html`, `cart.html`             |
| Lazy Loading Cart         | `pages/cart_view.py` (lazy import)             |
| /product/:id              | `templates/product.html`                       |

ตะกร้าเก็บใน session (ต่อผู้ใช้) ที่เดียวผ่าน `CartContext` ทุกหน้าจึงเห็นข้อมูลตรงกัน
