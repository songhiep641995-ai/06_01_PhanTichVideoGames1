import pandas as pd

def load_data(path):
    df = pd.read_csv(path)
    return df

def describe_data(df):
    print("=" * 40)
    print(f"Số dòng x số cột: {df.shape}")
    print()
    print("Kiểu dữ liệu từng cột:")
    print(df.dtypes)
    print()
    print("Số giá trị bị thiếu (null):")
    print(df.isnull().sum())
    print()
    print("Thống kê mô tả:")
    print(df.describe())
    print()
    print("5 dòng đầu tiên:")
    print(df.head())

# Chạy thử trực tiếp
if __name__ == "__main__":
    df = load_data('dataset/all_video_games_cleaned.csv')  # ← sửa đường dẫn
    describe_data(df)