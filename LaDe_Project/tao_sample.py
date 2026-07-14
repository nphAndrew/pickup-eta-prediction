import pandas as pd

print("Đang đọc file gốc...")
df = pd.read_csv('pickup_jl.csv')

# Lấy ngẫu nhiên 15.000 dòng để vẽ bản đồ cho mượt và nhẹ
df_small = df.sample(n=15000, random_state=42)

# Lưu ra file mới tên là pickup_small.csv
df_small.to_csv('pickup_small.csv', index=False)
print("🎉 Đã tạo xong file pickup_small.csv siêu nhẹ!")