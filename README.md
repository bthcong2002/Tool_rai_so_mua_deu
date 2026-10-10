# 📦 Ứng Dụng Rải Mua Đều Hàng Hóa

Ứng dụng web xây dựng bằng **Streamlit** giúp tự động hóa thuật toán rải mua đều hàng hóa theo quy cách mua và lịch về hàng của nhà cung cấp.

---

## 🚀 Tính Năng Chính
- **Giao diện thân thiện, trực quan:** Kéo thả upload file Excel (`.xlsx`, `.xls`).
- **Tự động rải số theo Quy Cách & Lịch Về Hàng :**
  - Lịch full tuần: Phân bổ vòng đều các phần nguyên, nhảy bước với phần dư.
  - Lịch cách ngày: Bắt đầu ngẫu nhiên theo nhịp và rải đều.
  - Xử lý phần lẻ chính xác, bảo toàn số lượng tổng mua.
- **Thống kê Dashboard tức thì:** Đếm tổng số dòng, tổng sản lượng mới, tổng đã rải và xác thực sai lệch 100%.
- **Xuất kết quả:** Xuất file Excel chuẩn (`Ket_qua_rai_mua_deuxlsx`) ngay trên trình duyệt.

---

## 🛠️ Cài Đặt & Chạy Cục Bộ (Local)

1. Clone repository:
```bash
git clone <URL_REPO_CUA_BAN>
cd <THU_MUC_REPO>
```

2. Cài đặt các thư viện phụ thuộc:
```bash
pip install -r requirements.txt
```

3. Chạy ứng dụng Streamlit:
```bash
streamlit run app.py
```

---

## 🌐 Hướng Dẫn Deploy Lên Streamlit Cloud

1. Tạo một repository mới trên GitHub (ví dụ: `rai-mua-deu-mwg`).
2. Đẩy toàn bộ mã nguồn lên GitHub:
```bash
git init
git add .
git commit -m "Initial commit for Rai Mua Deu Streamlit App"
git branch -M main
git remote add origin https://github.com/<tai-khoan-github>/<ten-repo>.git
git push -u origin main
```
3. Truy cập [share.streamlit.io](https://share.streamlit.io/) và đăng nhập bằng tài khoản GitHub.
4. Nhấn **New app**:
   - **Repository:** Chọn repository bạn vừa push (`<tai-khoan-github>/<ten-repo>`).
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Nhấn **Deploy** và chia sẻ đường link cho đội ngũ sử dụng!
