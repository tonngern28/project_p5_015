# ขั้นที่ 1: นำเข้า escape เพื่อแปลงอักขระพิเศษ (เช่น < > &) ให้ปลอดภัยก่อนใส่ใน HTML
from html import escape


def color_class(color: str) -> str:
    """แปลงรหัสสีเป็นชื่อคลาส CSS
    ตัวอย่าง: "#ff6b6b" -> "c-ff6b6b"
    (ใช้ชื่อคลาสแทน inline style ตามข้อห้ามของโจทย์)
    """
    return "c-" + color.lstrip("#").lower()


def color_css(colors) -> str:
    """สร้างกฎ CSS ของแต่ละสี (หนึ่งสีต่อหนึ่งกฎ) เช่น
    .c-ff6b6b { --accent: #ff6b6b; }
    ใช้ set() เพื่อตัดสีที่ซ้ำกันออก
    """
    return "\n".join(
        f".{color_class(c)} {{ --accent: {c}; }}" for c in sorted(set(colors))
    )


def ProfileCard(name: str, role: str, emoji: str, color: str, theme: str = "light") -> str:
    """คอมโพเนนต์การ์ดแนะนำตัว (คืนค่าเป็นข้อความ HTML)

    Props (พารามิเตอร์ที่รับเข้ามา):
      name  : ชื่อสมาชิก เช่น "สมชาย"
      role  : บทบาท/ตำแหน่ง เช่น "หัวหน้าชมรม"
      emoji : อีโมจิแทนตัว เช่น "🎮"
      color : สีหลักของการ์ด เช่น "#ff6b6b"
      theme : (Bonus) "light" หรือ "dark" ค่าเริ่มต้นคือ "light"
    """
    # ขั้นที่ 2: ประกอบ HTML ของการ์ดด้วย f-string
    # - class: คลาสหลัก + คลาสธีม + คลาสสี (สีถูกกำหนดในไฟล์ CSS ไม่ใช่ inline style)
    # - data-name: เก็บชื่อไว้ให้ปุ่มทักทายนำไปแสดงใน alert
    return f"""
    <div class="profile-card theme-{theme} {color_class(color)}">
      <div class="profile-card__avatar">{escape(emoji)}</div>
      <h2 class="profile-card__name">{escape(name)}</h2>
      <p class="profile-card__role">{escape(role)}</p>
      <button class="profile-card__btn" data-name="{escape(name)}">ทักทาย</button>
    </div>
    """
