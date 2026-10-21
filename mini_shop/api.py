"""
api.py
======
ดึงข้อมูลสินค้าจาก https://fakestoreapi.com (API จริง)
ใช้ urllib ของ Python มาตรฐาน ไม่ต้องติดตั้งไลบรารีเพิ่ม
"""

import json
import urllib.request
import urllib.error

API_BASE = "https://fakestoreapi.com"


class ApiError(Exception):
    """ข้อผิดพลาดเมื่อเรียก API ไม่สำเร็จ (เทียบเท่า error state ใน React)"""


def _get_json(url: str):
    """เรียก GET แล้วแปลง JSON เป็น Python object; timeout 10 วินาที"""
    # บาง API บล็อก User-Agent เริ่มต้นของ Python จึงกำหนดเอง
    req = urllib.request.Request(url, headers={"User-Agent": "MiniShop/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        raise ApiError(f"เรียก API ไม่สำเร็จ: {e}") from e


def fetch_products(limit: int = 8) -> list:
    """ดึงรายการสินค้า (ค่าเริ่มต้น 8 ชิ้นตามโจทย์)"""
    return _get_json(f"{API_BASE}/products?limit={limit}")


def fetch_product(product_id: int) -> dict:
    """ดึงสินค้า 1 ชิ้นตาม id (ใช้ในหน้ารายละเอียด และตอนเพิ่มลงตะกร้า)"""
    data = _get_json(f"{API_BASE}/products/{product_id}")
    if not data:
        raise ApiError("ไม่พบสินค้า")
    return data
