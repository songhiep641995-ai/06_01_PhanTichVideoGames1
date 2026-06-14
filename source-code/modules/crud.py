import pandas as pd


# ============================================================
#  BƯỚC 3 — CRUD OPERATIONS
#  Làm việc trên file đã xử lý: all_video_games_final.csv
# ============================================================


# --- CREATE ---
def create_record(df, title, release_date='', developer='Unknown',
                  publisher='Unknown', genres='', product_rating='Not Rated',
                  user_score=None, user_ratings_count=0, platforms_info='[]'):
    """Thêm một game mới vào DataFrame. Kiểm tra trùng tên trước khi thêm."""
    if title in df['Title'].values:
        print(f"[!] Game '{title}' đã tồn tại. Không thêm.")
        return df

    # Tính Score Category cho dòng mới
    if user_score is None or pd.isna(user_score):
        score_cat = 'Không rõ'
    elif user_score < 6:
        score_cat = 'Thấp'
    elif user_score <= 7.5:
        score_cat = 'Trung bình'
    else:
        score_cat = 'Cao'

    import re
    year_match = re.search(r'\d{4}', str(release_date))
    release_year = int(year_match.group()) if year_match else None
    game_age = 2025 - release_year if release_year else None

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
        'Release Year'      : release_year,
        'Game Age'          : game_age,
        'Score Category'    : score_cat,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    print(f"[✓] Đã thêm: '{title}' | Score Category: {score_cat} | Game Age: {game_age}")
    print(f"    Tổng hiện tại: {len(df)} dòng")
    return df


# --- READ ---
def read_all(df, n=10):
    """Hiển thị n dòng đầu."""
    print(f"\n[READ] {n} dòng đầu tiên:")
    print(df[['Title', 'Developer', 'Genres', 'User Score', 'Score Category']].head(n).to_string())
    return df.head(n)


def read_by_title(df, keyword):
    """Tìm game theo từ khóa tên (không phân biệt hoa/thường)."""
    result = df[df['Title'].str.contains(keyword, case=False, na=False)]
    print(f"\n[READ] Từ khóa '{keyword}' → {len(result)} kết quả:")
    if len(result) > 0:
        print(result[['Title', 'Developer', 'User Score', 'Score Category', 'Game Age']].to_string())
    return result


def read_by_genre(df, genre):
    """Lọc game theo thể loại."""
    result = df[df['Genres'].str.contains(genre, case=False, na=False)]
    print(f"\n[READ] Thể loại '{genre}' → {len(result)} game:")
    if len(result) > 0:
        print(result[['Title', 'Genres', 'User Score', 'Score Category']].head(10).to_string())
    return result


def read_by_score_category(df, category):
    """Lọc game theo Score Category: Thấp / Trung bình / Cao."""
    result = df[df['Score Category'] == category]
    print(f"\n[READ] Score Category '{category}' → {len(result)} game:")
    if len(result) > 0:
        print(result[['Title', 'User Score', 'Score Category', 'Release Year']].head(10).to_string())
    return result


def read_top_scores(df, n=10):
    """Top n game User Score cao nhất."""
    result = df.sort_values('User Score', ascending=False).head(n)
    print(f"\n[READ] Top {n} game điểm cao nhất:")
    print(result[['Title', 'Developer', 'User Score', 'Score Category']].to_string())
    return result


# --- UPDATE ---
def update_record(df, title, column, new_value):
    """Cập nhật một cột cho game theo tên chính xác."""
    mask = df['Title'] == title
    if mask.sum() == 0:
        print(f"[!] Không tìm thấy game '{title}'.")
        return df
    if column not in df.columns:
        print(f"[!] Cột '{column}' không tồn tại.")
        return df

    old_value = df.loc[mask, column].values[0]
    df.loc[mask, column] = new_value

    # Nếu sửa User Score thì tự cập nhật Score Category
    if column == 'User Score':
        try:
            s = float(new_value)
            cat = 'Thấp' if s < 6 else ('Trung bình' if s <= 7.5 else 'Cao')
            df.loc[mask, 'Score Category'] = cat
            print(f"[✓] Cập nhật '{title}': {column} = {old_value} → {new_value} | Score Category → {cat}")
        except:
            print(f"[✓] Cập nhật '{title}': {column} = '{old_value}' → '{new_value}'")
    else:
        print(f"[✓] Cập nhật '{title}': {column} = '{old_value}' → '{new_value}'")
    return df


# --- DELETE ---
def delete_record(df, title):
    """Xóa game theo tên chính xác."""
    mask = df['Title'] == title
    count = mask.sum()
    if count == 0:
        print(f"[!] Không tìm thấy '{title}' để xóa.")
        return df
    df = df[~mask].reset_index(drop=True)
    print(f"[✓] Đã xóa {count} dòng '{title}' → còn {len(df)} dòng")
    return df


# --- LƯU ---
def save_data(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"\n[✓] Đã lưu: {output_path}")


# ============================================================
#  CHẠY THỬ
# ============================================================
if __name__ == "__main__":
    INPUT_PATH  = 'dataset/all_video_games_final.csv'
    OUTPUT_PATH = 'dataset/all_video_games_crud.csv'

    df = pd.read_csv(INPUT_PATH)

    print("=" * 50)
    print("  THỬ NGHIỆM CRUD")
    print("=" * 50)

    print("\n[ CREATE ]")
    df = create_record(df, title='My Indie Game 2025', release_date='6/1/2025',
                       developer='My Studio', publisher='Indie Pub',
                       genres='Action RPG', user_score=8.0, user_ratings_count=50)

    print("\n[ READ - Tìm theo tên ]")
    read_by_title(df, 'Mario')

    print("\n[ READ - Score Category Cao ]")
    read_by_score_category(df, 'Cao')

    print("\n[ READ - Top 5 điểm cao ]")
    read_top_scores(df, n=5)

    print("\n[ UPDATE ]")
    df = update_record(df, 'My Indie Game 2025', 'User Score', 9.5)

    print("\n[ DELETE ]")
    df = delete_record(df, 'My Indie Game 2025')

    save_data(df, OUTPUT_PATH)
