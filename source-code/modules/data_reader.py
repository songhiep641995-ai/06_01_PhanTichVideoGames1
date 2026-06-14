import pandas as pd


# ============================================================
#  BƯỚC 1 — ĐỌC & MÔ TẢ DỮ LIỆU
#  Dataset: all_video_games_cleaned.csv
# ============================================================


def load_data(path):
    """Đọc file CSV và trả về DataFrame."""
    df = pd.read_csv(path)
    print(f"[✓] Đã đọc file: {path}")
    print(f"    Số dòng: {df.shape[0]} | Số cột: {df.shape[1]}")
    return df


def describe_data(df):
    """Mô tả tổng quan bộ dữ liệu."""
    print("=" * 50)
    print("  THÔNG TIN TỔNG QUAN DỮ LIỆU")
    print("=" * 50)
    print(f"Số dòng x số cột: {df.shape}")
    print()
    print("Tên các cột:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    print()
    print("Kiểu dữ liệu từng cột:")
    print(df.dtypes)
    print()
    print("Số giá trị thiếu (isnull().sum()):")
    print(df.isnull().sum())
    print()
    print("Thống kê mô tả (describe):")
    print(df.describe())
    print()
    print("5 dòng đầu tiên:")
    print(df.head())


# ============================================================
#  CHẠY THỬ TRỰC TIẾP
# ============================================================
if __name__ == "__main__":
    INPUT_PATH = 'dataset/all_video_games_cleaned.csv'
    df = load_data(INPUT_PATH)
    describe_data(df)
