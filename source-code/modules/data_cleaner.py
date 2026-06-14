import pandas as pd


# ============================================================
#  XỬ LÝ DỮ LIỆU — đúng theo đề bài
#  3.1 Kiểm tra & làm sạch
#  3.2 Bảng giá trị thiếu & cách xử lý
#  3.3 Feature Engineering (tạo cột mới)
# ============================================================


def kiem_tra_du_lieu(df):
    """3.1 - Kiểm tra dữ liệu thiếu và trùng lặp."""
    print("=" * 50)
    print("  KIỂM TRA DỮ LIỆU")
    print("=" * 50)
    print(f"Tổng số dòng    : {len(df)}")
    print(f"Tổng số cột     : {len(df.columns)}")
    print()
    print("--- Số giá trị thiếu (isnull().sum()) ---")
    print(df.isnull().sum())
    print()
    print(f"--- Số dòng trùng lặp: {df.duplicated().sum()} ---")
    return df


def lam_sach_du_lieu(df):
    """3.1 - Làm sạch: xóa trùng, xóa dòng thiếu Title."""
    print("\n" + "=" * 50)
    print("  LÀM SẠCH DỮ LIỆU")
    print("=" * 50)

    truoc = len(df)

    # Xóa dòng trùng lặp hoàn toàn
    df = df.drop_duplicates(subset=['Title'])
    print(f"[1] Xóa trùng lặp (drop_duplicates): -{truoc - len(df)} dòng → còn {len(df)}")

    # Xóa dòng không có Title (bắt buộc)
    truoc2 = len(df)
    df = df.dropna(subset=['Title'])
    print(f"[2] Xóa dòng thiếu Title (dropna)  : -{truoc2 - len(df)} dòng → còn {len(df)}")

    return df


def chuan_hoa_du_lieu(df):
    """3.2 - Chuẩn hóa & xử lý giá trị thiếu theo bảng đề bài."""
    print("\n" + "=" * 50)
    print("  CHUẨN HÓA DỮ LIỆU")
    print("=" * 50)

    # Chuyển kiểu số
    df['User Score']         = pd.to_numeric(df['User Score'], errors='coerce')
    df['User Ratings Count'] = pd.to_numeric(df['User Ratings Count'], errors='coerce')

    # Release Date: fillna('Unknown') + chuyển sang datetime
    df['Release Date'] = df['Release Date'].fillna('Unknown')
    df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
    print("[3] Release Date → fillna('Unknown') + pd.to_datetime(errors='coerce')")

    # Developer, Publisher → fillna('Unknown')
    df['Developer'] = df['Developer'].fillna('Unknown')
    df['Publisher']  = df['Publisher'].fillna('Unknown')
    print("[4] Developer, Publisher → fillna('Unknown')")

    # Product Rating → fillna('Not Rated')
    df['Product Rating'] = df['Product Rating'].fillna('Not Rated')
    print("[5] Product Rating → fillna('Not Rated')")

    # User Score → fillna(median)
    median_score = df['User Score'].median()
    df['User Score'] = df['User Score'].fillna(median_score)
    print(f"[6] User Score → fillna(median={median_score})")

    # User Ratings Count → fillna(0)
    df['User Ratings Count'] = df['User Ratings Count'].fillna(0)
    print("[7] User Ratings Count → fillna(0)")

    print()
    print("Kiểu dữ liệu sau chuẩn hóa:")
    print(df.dtypes)

    return df


def feature_engineering(df):
    """3.3 - Tạo cột mới từ dữ liệu hiện có."""
    print("\n" + "=" * 50)
    print("  FEATURE ENGINEERING")
    print("=" * 50)

    # Cột Release Year
    df['Release Year'] = df['Release Date'].dt.year
    print("[8] Tạo cột Release Year = Release Date.dt.year")

    # Cột Game Age
    df['Game Age'] = 2025 - df['Release Year']
    print("[9] Tạo cột Game Age = 2025 - Release Year")

    # Cột Score Category
    def phan_loai(s):
        if pd.isna(s): return 'Không rõ'
        if s < 6:      return 'Thấp'
        if s <= 7.5:   return 'Trung bình'
        return 'Cao'

    df['Score Category'] = df['User Score'].apply(phan_loai)
    print("[10] Tạo cột Score Category: Thấp (<6) / Trung bình (6-7.5) / Cao (>7.5)")

    print()
    print("Phân bố Score Category:")
    print(df['Score Category'].value_counts())
    print()
    print("Mẫu 5 dòng đầu (cột mới):")
    print(df[['Title', 'Release Year', 'Game Age', 'Score Category']].head())

    return df


def thong_ke_sau_xu_ly(df):
    """In thống kê số dòng lỗi trước và sau xử lý."""
    print("\n" + "=" * 50)
    print("  KẾT QUẢ SAU XỬ LÝ")
    print("=" * 50)
    print(f"Tổng số dòng còn lại: {len(df)}")
    print()
    print("Giá trị null còn lại:")
    print(df.isnull().sum())


def save_clean_data(df, output_path):
    """Lưu dữ liệu đã xử lý ra file CSV."""
    df.to_csv(output_path, index=False)
    print(f"\n[✓] Đã lưu file tại: {output_path}")


# ============================================================
#  CHẠY THỬ TRỰC TIẾP
# ============================================================
if __name__ == "__main__":
    INPUT_PATH  = 'dataset/all_video_games_cleaned.csv'
    OUTPUT_PATH = 'dataset/all_video_games_final.csv'

    df = pd.read_csv(INPUT_PATH)

    df = kiem_tra_du_lieu(df)
    df = lam_sach_du_lieu(df)
    df = chuan_hoa_du_lieu(df)
    df = feature_engineering(df)
    thong_ke_sau_xu_ly(df)
    save_clean_data(df, OUTPUT_PATH)
