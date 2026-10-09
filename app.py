import io
import random
import numpy as np
import pandas as pd
import streamlit as st

# Cấu hình trang giao diện Streamlit
st.set_page_config(
    page_title="Hệ Thống Rải Mua Đều Hàng Hóa - Ver 4",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS cho giao diện hiện đại & chuyên nghiệp
st.markdown(
    """
    <style>
    /* Gradient Header */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    .main-header h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
    }
    .main-header p {
        margin: 8px 0 0 0;
        opacity: 0.9;
        font-size: 15px;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 16px 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    
    /* Guide box */
    .guide-box {
        background-color: #f8fafc;
        border-left: 4px solid #2a5298;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 20px;
        font-size: 14px;
        color: #334155;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Mapping thứ thành tên cột (0: 'sun', ..., 6: 'sat')
DAYS_MAPPING = {0: 'sun', 1: 'mon', 2: 'tue', 3: 'wed', 4: 'thu', 5: 'fri', 6: 'sat'}
DAYS_ORDER = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
DESIRED_ORDER = [
    'Mã siêu thị', 'Tên siêu thị', 'Mã sản phẩm', 'Tên sản phẩm', 'Map',
    'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN', 'Tổng cũ',
    'Quy cách mua', 'Lịch về hàng', 'Nhóm rải', 'Bước nhảy', 'Day start',
    'Tổng mới', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'
]


def distribute_by_quycach(row):
    """
    Thuật toán cốt lõi rải số mua đều theo Quy cách mua và Lịch về hàng (Ver 4)
    """
    lich_ve = row.get('Lịch về hàng')
    try:
        qck = float(row.get('Quy cách mua', 0))
        tong_moi = float(row.get('Tổng mới', 0))
    except (ValueError, TypeError):
        return row

    if pd.isnull(lich_ve) or qck <= 0 or pd.isnull(tong_moi) or tong_moi <= 0:
        return row

    try:
        days = sorted([int(x.strip()) for x in str(lich_ve).split(',') if x.strip() != ""])
    except Exception:
        return row

    if not days:
        return row

    # Khởi tạo các cột ngày về 0
    for d in DAYS_MAPPING.values():
        row[d] = 0

    so_quy_cach_rai = int(tong_moi // qck)  # số phần nguyên cần rải
    phan_le = tong_moi - so_quy_cach_rai * qck  # phần lẻ nhỏ
    len_days = len(days)

    def add_day_idx(idx):
        day_index = days[idx % len_days]
        row[DAYS_MAPPING[day_index]] += qck

    def rai_buoc_nhay(n, buoc, start):
        for i in range(n):
            add_day_idx((start + i * buoc) % len_days)

    # 1. Trường hợp lịch về hàng full tuần (7 ngày)
    if len_days == 7:
        if so_quy_cach_rai >= 7:
            vong = so_quy_cach_rai // 7
            so_phan_con_lai = so_quy_cach_rai % 7

            for _ in range(vong):
                for i in range(7):
                    add_day_idx(i)

            if so_phan_con_lai > 0:
                if so_phan_con_lai == 6:
                    buoc_nhay = 1
                elif so_phan_con_lai in [5, 4, 3]:
                    buoc_nhay = 2
                elif so_phan_con_lai == 2:
                    buoc_nhay = 4
                else:
                    buoc_nhay = 1
                day_start = random.randint(0, len_days - 1)
                rai_buoc_nhay(so_phan_con_lai, buoc_nhay, day_start)
            else:
                buoc_nhay = "vòng đều"
                day_start = "n/a"

            # Xử lý phần lẻ
            if phan_le > 0:
                if isinstance(day_start, int):
                    day_cho = days[day_start]
                else:
                    day_cho = days[0]
                row[DAYS_MAPPING[day_cho]] += phan_le

            row["Bước nhảy"] = buoc_nhay
            row["Day start"] = day_start
            return row

        else:
            # Trường hợp < 7 phần nguyên, rải nhảy cách ngày
            if so_quy_cach_rai == 6:
                buoc_nhay = 1
            elif so_quy_cach_rai in [5, 4, 3]:
                buoc_nhay = 2
            elif so_quy_cach_rai == 2:
                buoc_nhay = 4
            else:
                buoc_nhay = 1
            day_start = random.randint(0, len_days - 1)
            rai_buoc_nhay(so_quy_cach_rai, buoc_nhay, day_start)
            if phan_le > 0:
                day_cho = days[day_start]
                row[DAYS_MAPPING[day_cho]] += phan_le

            row["Bước nhảy"] = buoc_nhay
            row["Day start"] = day_start
            return row

    # 2. Trường hợp lịch về không full tuần (cách ngày)
    else:
        def rai_deu_offset(n, offset):
            for i in range(n):
                idx = (offset + i) % len_days
                day_idx = days[idx]
                row[DAYS_MAPPING[day_idx]] += qck

        start_pos = random.randint(0, len_days - 1)
        start_day = days[start_pos]

        # Rải đều toàn bộ các phần nguyên theo điểm xuất phát ngẫu nhiên
        rai_deu_offset(so_quy_cach_rai, start_pos)

        # Phần lẻ (< qck): rải vào 1 ngày ngẫu nhiên trong lịch
        if phan_le > 0:
            day_idx = random.choice(days)
            row[DAYS_MAPPING[day_idx]] += phan_le

        row["Bước nhảy"] = "vòng đều + dư random" if phan_le > 0 else "vòng đều"
        row["Day start"] = start_day
        return row


def process_rai_mua_deu(df):
    """Quy trình chuẩn hóa và xử lý rải số mua đều"""
    df_result = df.copy()

    # Đảm bảo đủ các cột ngày
    for col in DAYS_MAPPING.values():
        if col not in df_result.columns:
            df_result[col] = 0

    for col in DAYS_ORDER:
        if col not in df_result.columns:
            df_result[col] = 0

    # Phân nhóm rải
    if 'Lịch về hàng' in df_result.columns:
        df_result['Nhóm rải'] = np.where(
            df_result['Lịch về hàng'].astype(str).str.replace(" ", "") != '0,1,2,3,4,5,6',
            '1.Nhóm có lịch cách ngày',
            '2.Nhóm có lịch mỗi ngày'
        )

    # Sắp xếp
    sort_cols = [c for c in ['Tên sản phẩm', 'Nhóm rải', 'Tổng mới'] if c in df_result.columns]
    if sort_cols:
        df_result.sort_values(by=sort_cols, ascending=[True, True, False][:len(sort_cols)], inplace=True)
    df_result = df_result.reset_index(drop=True)

    # Chạy phân bổ rải đều
    df_result = df_result.apply(distribute_by_quycach, axis=1)

    # Sắp xếp thứ tự các cột mong muốn nếu có
    existing_desired = [col for col in DESIRED_ORDER if col in df_result.columns]
    other_cols = [col for col in df_result.columns if col not in existing_desired]
    final_cols = existing_desired + other_cols

    return df_result[final_cols]


# ---------------------------------------------
# SIDEBAR
# ---------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2897/2897785.png", width=64)
    st.title("Cấu hình & Tùy chọn")
    
    st.markdown("---")
    st.subheader("📌 Yêu cầu file đầu vào:")
    st.markdown(
        """
        File Excel (`.xlsx` hoặc `.xls`) cần chứa tối thiểu các cột:
        - **`Lịch về hàng`** (ví dụ: `0,1,2,3,4,5,6` hoặc `1,3,5`)
        - **`Quy cách mua`** (ví dụ: `6`, `12`, `24`)
        - **`Tổng mới`** (Số lượng cần mua rải trong tuần)
        - *(Tùy chọn: Mã siêu thị, Tên sản phẩm, Tổng cũ...)*
        """
    )

    st.markdown("---")
    st.info("💡 **Gợi ý quy ước Thứ trong tuần:**\n- `0`: Chủ Nhật\n- `1`: Thứ Hai\n- `2`: Thứ Ba\n- `3`: Thứ Tư\n- `4`: Thứ Năm\n- `5`: Thứ Sáu\n- `6`: Thứ Bảy")


# ---------------------------------------------
# MAIN APP INTERFACE
# ---------------------------------------------
st.markdown(
    """
    <div class="main-header">
        <h1>📦 Rải Mua Đều Hàng Hóa (Ver 4)</h1>
        <p>Hệ thống tự động phân bổ sản lượng mua đều theo Quy cách mua & Lịch giao hàng của Nhà cung cấp</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Upload Section
uploaded_file = st.file_uploader(
    "📥 Tải lên file Excel cần rải số (Định dạng: .xlsx, .xls)",
    type=["xlsx", "xls"],
    help="Chọn file Excel chứa các cột Lịch về hàng, Quy cách mua, Tổng mới",
)

if uploaded_file is not None:
    try:
        # Đọc dữ liệu từ file upload
        xl = pd.ExcelFile(uploaded_file)
        sheet_names = xl.sheet_names

        col1, col2 = st.columns([2, 1])
        with col1:
            selected_sheet = st.selectbox("📑 Chọn Sheet dữ liệu:", sheet_names, index=0)
        with col2:
            st.write("")
            st.write("")
            run_btn = st.button("🚀 Bắt đầu Rải Số", type="primary", use_container_width=True)

        df_input = pd.read_excel(uploaded_file, sheet_name=selected_sheet)

        # Kiểm tra cột bắt buộc
        required_cols = ['Lịch về hàng', 'Quy cách mua', 'Tổng mới']
        missing_cols = [c for c in required_cols if c not in df_input.columns]

        if missing_cols:
            st.error(f"⚠️ File thiếu các cột bắt buộc: `{', '.join(missing_cols)}`. Vui lòng kiểm tra lại cấu trúc file!")
        else:
            # Hiển thị Preview ban đầu
            with st.expander("👀 Xem trước dữ liệu tải lên (10 dòng đầu)", expanded=False):
                st.dataframe(df_input.head(10), use_container_width=True)

            # Thực thi thuật toán
            if run_btn or 'processed_df' in st.session_state:
                if run_btn:
                    with st.spinner("Đang tính toán rải đều theo quy cách..."):
                        processed_df = process_rai_mua_deu(df_input)
                        st.session_state['processed_df'] = processed_df
                else:
                    processed_df = st.session_state['processed_df']

                st.success("✅ Đã xử lý rải số mua đều thành công!")

                # Hiển thị tóm tắt Dashboard
                st.markdown("### 📊 Thống Kê Tổng Quan")
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.metric("Tổng số dòng", f"{len(processed_df):,}")
                with m2:
                    total_new = processed_df['Tổng mới'].sum() if 'Tổng mới' in processed_df.columns else 0
                    st.metric("Tổng SL Mới", f"{total_new:,.2f}")
                with m3:
                    dist_cols = [d for d in DAYS_ORDER if d in processed_df.columns]
                    total_rai = processed_df[dist_cols].sum().sum() if dist_cols else 0
                    st.metric("Tổng SL Đã Rải", f"{total_rai:,.2f}")
                with m4:
                    diff = abs(total_new - total_rai)
                    st.metric("Chênh lệch kiểm tra", f"{diff:,.2f}", delta="Khớp 100%" if diff < 0.01 else "Lệch", delta_color="normal" if diff < 0.01 else "inverse")

                # Bảng chi tiết kết quả
                st.markdown("### 📋 Kết Quả Phân Bổ")
                st.dataframe(
                    processed_df,
                    use_container_width=True,
                    height=450,
                )

                # Nút tải file Excel kết quả
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    processed_df.to_excel(writer, index=False, sheet_name='Ket_qua_rai_mua_deu')
                buffer.seek(0)

                st.download_button(
                    label="💾 Tải Xuống File Kết Quả (.xlsx)",
                    data=buffer,
                    file_name="Ket_qua_rai_mua_deu_ver4.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary",
                    use_container_width=True,
                )

    except Exception as e:
        st.error(f"❌ Có lỗi trong quá trình xử lý file: {str(e)}")
else:
    st.info("👆 Vui lòng tải lên file Excel để bắt đầu trải nghiệm.")
