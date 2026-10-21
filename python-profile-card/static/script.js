// ==========================================================
// script.js - ส่วนโต้ตอบของหน้าเว็บ (ปุ่มทักทาย + ปุ่มสลับโหมด)
// ==========================================================

// ขั้นที่ 1: ดึงองค์ประกอบที่ต้องใช้จากหน้าเว็บ
const app = document.querySelector(".app");
const toggleBtn = document.querySelector(".theme-toggle");

// ขั้นที่ 2: เก็บธีมปัจจุบันไว้ในตัวแปร (เริ่มต้นเป็นโหมดสว่าง)
let theme = "light";

// ขั้นที่ 3: ฟังก์ชันนำธีมไปใช้กับทั้งหน้าและการ์ดทุกใบ
function applyTheme() {
  // เปลี่ยนคลาสของหน้าหลัก เช่น app--dark
  app.className = `app app--${theme}`;

  // วนเปลี่ยนคลาสธีมของการ์ดทุกใบ
  document.querySelectorAll(".profile-card").forEach((card) => {
    card.classList.remove("theme-light", "theme-dark");
    card.classList.add(`theme-${theme}`);
  });

  // เปลี่ยนข้อความบนปุ่มให้ตรงกับโหมดที่จะสลับไป
  toggleBtn.textContent = theme === "light" ? "🌙 โหมดมืด" : "☀️ โหมดสว่าง";
}

// ขั้นที่ 4: เมื่อกดปุ่มสลับโหมด ให้สลับ light <-> dark แล้วนำไปใช้
toggleBtn.addEventListener("click", () => {
  theme = theme === "light" ? "dark" : "light";
  applyTheme();
});

// ขั้นที่ 5: (Bonus) ปุ่มทักทาย - ผูกเหตุการณ์คลิกกับปุ่มของทุกการ์ด
document.querySelectorAll(".profile-card__btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    // อ่านชื่อจาก data-name แล้วแสดงใน alert
    alert("สวัสดี ฉันชื่อ " + btn.dataset.name);
  });
});
