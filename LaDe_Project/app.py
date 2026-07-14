import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# 1. Cài đặt tiêu đề và giao diện cho Web App
st.set_page_config(page_title="Bản đồ Nhiệt Shipper", layout="wide")
st.title("🗺️ Bản đồ Mật độ (Heatmap) của Shipper")
# Tạo thanh công cụ bên trái
st.sidebar.header("⚙️ Tùy chỉnh Bản đồ")

# Thêm thanh kéo (slider)
ban_kinh = st.sidebar.slider("Chỉnh kích thước vùng nhiệt (Radius)", min_value=5, max_value=30, value=14)

# BẠN CẦN SỬA LẠI DÒNG HEATMAP CŨ THÀNH NHƯ SAU:
# HeatMap(heat_data, radius=ban_kinh, blur=10).add_to(m)
st.markdown("Bản đồ dưới đây hiển thị các khu vực tập trung đông đúc các điểm lấy/giao hàng dựa trên dữ liệu.")

# 2. Đọc dữ liệu
# Streamlit cache giúp ứng dụng không phải đọc lại file csv mỗi khi bạn tương tác
@st.cache_data
def load_data():
    # Đọc file CSV trong thư mục hiện tại
    df = pd.read_csv('c:\\Users\\ADMIN\\Downloads\\pickup_jl.csv') 
    return df

try:
    df = load_data()

    # THAY ĐỔI TÊN CỘT Ở ĐÂY CHO KHỚP VỚI FILE CSV CỦA BẠN (vd: 'lat', 'lon')
    lat_col = 'pickup_gps_lat'  
    lon_col = 'pickup_gps_lng' 

    # Lọc bỏ các dòng bị thiếu tọa độ và tạo list dữ liệu cho Heatmap
    heat_data = df[[lat_col, lon_col]].dropna().values.tolist()

    # 3. Khởi tạo bản đồ Folium
    # Lấy tọa độ trung bình để tự động căn giữa bản đồ
    center_lat = df[lat_col].mean()
    center_lon = df[lon_col].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

    # 4. Thêm lớp Heatmap vào bản đồ
    # Có thể tùy chỉnh radius (độ to của điểm nhiệt) và blur (độ mờ/nhòe)
    HeatMap(heat_data, radius=14, blur=10).add_to(m)

    # 5. Hiển thị bản đồ lên giao diện Streamlit
    st_folium(m, width=900, height=500)

except FileNotFoundError:
    st.error("Lỗi: Không tìm thấy file 'pickup_jl.csv'.")
except KeyError:
    st.error(f"Lỗi: Không tìm thấy cột '{lat_col}' hoặc '{lon_col}'. Vui lòng mở file CSV xem tên cột tọa độ là gì và sửa lại trong code!")