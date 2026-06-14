import pandas as pd


# ============================================================
#  BƯỚC 2 — LÀM SẠCH & CHUẨN HÓA DỮ LIỆU
#  Dataset: all_video_games_cleaned.csv
# ============================================================

RATING_MAP = {
    'Rated E For Everyone'        : 'E',
    'Rated T For Teen'            : 'T',
    'Rated M For Mature'          : 'M',
    'Rated E +10 For Everyone +10': 'E10+',
    'Rated RP For Rate Pending'   : 'RP',
    'Rated AO For Adults Only'    : 'AO',
}


def remove_duplicates(df):
    """Xóa các dòng bị trùng lặp hoàn toàn."""
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"[1] Xóa trùng lặp: {before - after} dòng bị loại → còn {after} dòng")
    return df


def remove_missing_titles(df):
    """Xóa các dòng không có tên game (Title là bắt buộc)."""
    before = len(df)
    df = df.dropna(subset=['Title'])
    after = len(df)
    print(f"[2] Xóa dòng thiếu Title: {before - after} dòng bị loại → còn {after} dòng")
    return df


def convert_data_types(df):
    """Chuyển đổi kiểu dữ liệu cho đúng."""
    df['User Score']        = pd.to_numeric(df['User Score'], errors='coerce')
    df['User Ratings Count']= pd.to_numeric(df['User Ratings Count'], errors='coerce')
    df['Release Date']      = pd.to_datetime(df['Release Date'], errors='coerce')
    print("[3] Chuyển kiểu dữ liệu:")
    print(f"    User Score       → float64")
    print(f"    User Ratings Count → float64")
    print(f"    Release Date     → datetime64")
    return df


def normalize_product_rating(df):
    """Rút gọn nhãn Product Rating cho dễ xử lý (vd: 'Rated T For Teen' → 'T')."""
    df['Product Rating'] = df['Product Rating'].map(RATING_MAP)
    print("[4] Chuẩn hóa Product Rating → E / T / M / E10+ / RP / AO")
    return df


def fill_missing_text(df):
    """Điền 'Unknown' vào các cột text bị thiếu không quan trọng."""
    df['Developer'] = df['Developer'].fillna('Unknown')
    df['Publisher']  = df['Publisher'].fillna('Unknown')
    print("[5] Điền 'Unknown' cho Developer/Publisher bị thiếu")
    return df


def clean_data(df):
    """Gọi toàn bộ các bước làm sạch theo thứ tự."""
    print("=" * 45)
    print("  BẮT ĐẦU LÀM SẠCH DỮ LIỆU")
    print("=" * 45)
    print(f"Số dòng ban đầu: {len(df)}")
    print()

    df = remove_duplicates(df)
    df = remove_missing_titles(df)
    df = convert_data_types(df)
    df = normalize_product_rating(df)
    df = fill_missing_text(df)

    print()
    print("=" * 45)
    print(f"  KẾT QUẢ SAU KHI LÀM SẠCH")
    print("=" * 45)
    print(f"Số dòng còn lại : {len(df)}")
    print()
    print("Giá trị null còn lại:")
    print(df.isnull().sum())
    print()
    print("Phân bố Product Rating:")
    print(df['Product Rating'].value_counts())
    print()
    print("Kiểu dữ liệu các cột:")
    print(df.dtypes)
    return df


def save_clean_data(df, output_path):
    """Lưu dữ liệu đã làm sạch ra file CSV mới."""
    df.to_csv(output_path, index=False)
    print(f"\n[✓] Đã lưu file sạch tại: {output_path}")


# ============================================================
#  CHẠY THỬ TRỰC TIẾP
# ============================================================
if __name__ == "__main__":
    # ← Sửa đường dẫn cho phù hợp máy bạn
    INPUT_PATH  = 'dataset/all_video_games_cleaned.csv'
    OUTPUT_PATH = 'dataset/all_video_games_final.csv'

    df_raw   = pd.read_csv(INPUT_PATH)
    df_clean = clean_data(df_raw)
    save_clean_data(df_clean, OUTPUT_PATH)