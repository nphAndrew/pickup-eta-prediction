import os
import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# 1. Cài đặt tiêu đề và giao diện cho Web App
st.set_page_config(page_title="Bản đồ Nhiệt Shipper", layout="wide")
st.title("🗺️ Bản đồ Mật độ (Heatmap) của Shipper")

# Tạo thanh công cụ bên trái (Sidebar)
st.sidebar.header("⚙️ Tùy chỉnh Bản đồ")

# Thêm thanh kéo (slider) để lấy giá trị bán kính từ người dùng
ban_kinh = st.sidebar.slider("Chỉnh kích thước vùng nhiệt (Radius)", min_value=5, max_value=30, value=14)

st.markdown("Bản đồ dưới đây hiển thị các khu vực tập trung đông đúc các điểm lấy/giao hàng dựa trên dữ liệu.")

# 2. Đọc dữ liệu
# Streamlit cache giúp ứng dụng không phải đọc lại file csv mỗi khi bạn tương tác
@st.cache_data
def load_data():
    # Sử dụng os.path để code tự tìm file trong cùng thư mục với file app.py,
    # giúp chạy mượt mà cả ở máy cá nhân lẫn trên máy chủ Streamlit Cloud.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'pickup_jl.csv')
    
    # Trường hợp dự phòng: nếu chạy cục bộ mà chưa có file bên cạnh, tìm ở thư mục LaDe_Project
    if not os.path.exists(file_path) and os.path.exists('LaDe_Project/pickup_jl.csv'):
        file_path = 'LaDe_Project/pickup_jl.csv'
        
    df = pd.read_csv(file_path) 
    return df

try:
    df = load_data()

    # THAY ĐỔI TÊN CỘT Ở ĐÂY CHO KHỚP VỚI FILE CSV CỦA BẠN
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
    # Đã thay số cố định bằng biến `ban_kinh` để bản đồ thay đổi khi kéo slider
    HeatMap(heat_data, radius=ban_kinh, blur=10).add_to(m)

    # 5. Hiển thị bản đồ lên giao diện Streamlit
    st_folium(m, width=900, height=500)

except FileNotFoundError:
    st.error("Lỗi: Không tìm thấy file 'pickup_jl.csv'. Vui lòng đảm bảo file CSV nằm cùng thư mục với file app.py hoặc tải nó lên GitHub.")
except KeyError:
    st.error(f"Lỗi: Không tìm thấy cột '{lat_col}' hoặc '{lon_col}'. Vui lòng mở file CSV xem tên cột tọa độ là gì và sửa lại trong code!")
