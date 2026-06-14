import pandas as pd


# ============================================================
#  BƯỚC 3 — CRUD OPERATIONS
#  Dataset: all_video_games_cleaned.csv
#  Create / Read / Update / Delete
# ============================================================


# ------------------------------------------------------------
#  CREATE — Thêm game mới vào dataset
# ------------------------------------------------------------
def create_record(df, title, release_date='', developer='Unknown',
                  publisher='Unknown', genres='', product_rating='',
                  user_score=None, user_ratings_count=None, platforms_info='[]'):
    """
    Thêm một game mới vào cuối DataFrame.
    Trả về DataFrame mới (có game vừa thêm).
    """
    # Kiểm tra game đã tồn tại chưa
    if title in df['Title'].values:
        print(f"[!] Game '{title}' đã tồn tại trong dataset. Không thêm.")
        return df

    new_row = {
        'Title'             : title,
        'Release Date'      : release_date,
        'Developer'         : developer,
        'Publisher'         : publisher,
        'Genres'            : genres,
        'Product Rating'    : product_rating,
        'User Score'        : user_score,
        'User Ratings Count': user_ratings_count,
        'Platforms Info'    : platforms_info,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    print(f"[✓] Đã thêm game: '{title}' (tổng: {len(df)} dòng)")
    return df


# ------------------------------------------------------------
#  READ — Đọc / Tìm kiếm dữ liệu
# ------------------------------------------------------------
def read_all(df, n=10):
    """Hiển thị n dòng đầu tiên."""
    print(f"[READ] Hiển thị {n} dòng đầu:")
    print(df[['Title', 'Developer', 'Genres', 'User Score']].head(n).to_string())
    return df.head(n)


def read_by_title(df, keyword):
    """Tìm game theo từ khóa trong tên (không phân biệt hoa/thường)."""
    result = df[df['Title'].str.contains(keyword, case=False, na=False)]
    print(f"[READ] Tìm '{keyword}' → {len(result)} kết quả:")
    if len(result) > 0:
        print(result[['Title', 'Developer', 'Publisher', 'User Score']].to_string())
    return result


def read_by_genre(df, genre):
    """Lọc game theo thể loại."""
    result = df[df['Genres'].str.contains(genre, case=False, na=False)]
    print(f"[READ] Thể loại '{genre}' → {len(result)} game:")
    if len(result) > 0:
        print(result[['Title', 'Genres', 'User Score']].head(10).to_string())
    return result


def read_by_rating(df, rating):
    """Lọc game theo mức xếp hạng (E, T, M, E10+, RP, AO)."""
    result = df[df['Product Rating'] == rating]
    print(f"[READ] Rating '{rating}' → {len(result)} game")
    if len(result) > 0:
        print(result[['Title', 'Product Rating', 'User Score']].head(10).to_string())
    return result


def read_top_scores(df, n=10):
    """Lấy top n game có User Score cao nhất."""
    result = df.dropna(subset=['User Score']).sort_values('User Score', ascending=False).head(n)
    print(f"[READ] Top {n} game User Score cao nhất:")
    print(result[['Title', 'Developer', 'User Score', 'User Ratings Count']].to_string())
    return result


# ------------------------------------------------------------
#  UPDATE — Cập nhật thông tin một game
# ------------------------------------------------------------
def update_record(df, title, column, new_value):
    """
    Cập nhật giá trị của một cột cho game theo tên.
    Trả về DataFrame đã cập nhật.
    """
    mask = df['Title'] == title

    if mask.sum() == 0:
        print(f"[!] Không tìm thấy game '{title}'.")
        return df

    if column not in df.columns:
        print(f"[!] Cột '{column}' không tồn tại. Các cột hợp lệ: {list(df.columns)}")
        return df

    old_value = df.loc[mask, column].values[0]
    df.loc[mask, column] = new_value
    print(f"[✓] Cập nhật '{title}': {column} = '{old_value}' → '{new_value}'")
    return df


# ------------------------------------------------------------
#  DELETE — Xóa game khỏi dataset
# ------------------------------------------------------------
def delete_record(df, title):
    """
    Xóa tất cả dòng có tên game khớp chính xác.
    Trả về DataFrame đã xóa.
    """
    mask = df['Title'] == title
    count = mask.sum()

    if count == 0:
        print(f"[!] Không tìm thấy game '{title}' để xóa.")
        return df

    df = df[~mask].reset_index(drop=True)
    print(f"[✓] Đã xóa {count} dòng game '{title}' (còn lại: {len(df)} dòng)")
    return df


# ------------------------------------------------------------
#  LƯU FILE
# ------------------------------------------------------------
def save_data(df, output_path):
    """Lưu DataFrame ra file CSV sau khi thao tác CRUD."""
    df.to_csv(output_path, index=False)
    print(f"\n[✓] Đã lưu file tại: {output_path}")


# ============================================================
#  CHẠY THỬ TRỰC TIẾP
# ============================================================
if __name__ == "__main__":
    INPUT_PATH  = 'dataset/all_video_games_final.csv'   # ← file đã clean ở bước 2
    OUTPUT_PATH = 'dataset/all_video_games_crud.csv'

    df = pd.read_csv(INPUT_PATH)

    print("=" * 50)
    print("  THỬ NGHIỆM CÁC THAO TÁC CRUD")
    print("=" * 50)

    # --- CREATE ---
    print("\n[ CREATE ]")
    df = create_record(
        df,
        title='My Indie Game 2025',
        release_date='6/1/2025',
        developer='My Studio',
        publisher='Indie Pub',
        genres='Action RPG',
        product_rating='T',
        user_score=7.5,
        user_ratings_count=50
    )

    # --- READ ---
    print("\n[ READ - Tìm theo tên ]")
    read_by_title(df, 'Mario')

    print("\n[ READ - Lọc theo thể loại ]")
    read_by_genre(df, 'RPG')

    print("\n[ READ - Top 5 điểm cao nhất ]")
    read_top_scores(df, n=5)

    # --- UPDATE ---
    print("\n[ UPDATE ]")
    df = update_record(df, 'My Indie Game 2025', 'User Score', 9.0)

    # --- DELETE ---
    print("\n[ DELETE ]")
    df = delete_record(df, 'My Indie Game 2025')

    # --- LƯU ---
    save_data(df, OUTPUT_PATH)