import pandas as pd
from tkinter import messagebox

# ==========================
# DATA CLEANING
# ==========================

def clean_data(refresh_table):

    try:

        path = r"D:/LapTrinhPython/DOAN/VideoGamesProject/dataset/all_video_games(cleaned)_full.csv"

        # ==========================
        # BƯỚC 1: ĐỌC DỮ LIỆU
        # ==========================

        df = pd.read_csv(path)

        original_rows = len(df)

        # ==========================
        # BƯỚC 2: XÓA DỮ LIỆU TRÙNG LẶP
        # ==========================

        duplicate_count = df.duplicated().sum()

        df.drop_duplicates(
            inplace=True
        )

        # ==========================
        # BƯỚC 3: XÓA DỮ LIỆU THIẾU TITLE
        # ==========================

        missing_title = df["Title"].isna().sum()

        df.dropna(
            subset=["Title"],
            inplace=True
        )

        # ==========================
        # BƯỚC 4: XỬ LÝ GIÁ TRỊ THIẾU
        # ==========================

        developer_null = df["Developer"].isna().sum()

        publisher_null = df["Publisher"].isna().sum()

        genres_null = df["Genres"].isna().sum()

        df["Developer"] = df["Developer"].fillna(
            "Unknown"
        )

        df["Publisher"] = df["Publisher"].fillna(
            "Unknown"
        )

        df["Genres"] = df["Genres"].fillna(
            "Unknown"
        )

        # ==========================
        # BƯỚC 5: CHUẨN HÓA KIỂU DỮ LIỆU
        # ==========================

        df["User Score"] = pd.to_numeric(
            df["User Score"],
            errors="coerce"
        )

        df["User Ratings Count"] = pd.to_numeric(
            df["User Ratings Count"],
            errors="coerce"
        )

        # ==========================
        # BƯỚC 6: CHUẨN HÓA NGÀY THÁNG
        # ==========================

        df["Release Date"] = pd.to_datetime(
            df["Release Date"],
            errors="coerce"
        )

        df["Release Date"] = (
            df["Release Date"]
            .dt.strftime("%Y-%m-%d")
        )

        # ==========================
        # BƯỚC 7: CHUẨN HÓA ESRB
        # ==========================

        rating_map = {

            "Rated E For Everyone": "E",

            "Rated E10+ For Everyone 10+": "E10+",

            "Rated T For Teen": "T",

            "Rated M For Mature 17+": "M",

            "Rated AO For Adults Only": "AO",

            "Rated EC For Early Childhood": "EC",

            "Rated RP For Rating Pending": "RP"

        }

        df["Product Rating"] = (
            df["Product Rating"]
            .replace(rating_map)
        )

        # ==========================
        # BƯỚC 8: RESET INDEX
        # ==========================

        df.reset_index(
            drop=True,
            inplace=True
        )

        # ==========================
        # BƯỚC 9: LƯU FILE CSV
        # ==========================

        df.to_csv(
            path,
            index=False
        )

        # ==========================
        # BƯỚC 10: CẬP NHẬT GIAO DIỆN
        # ==========================

        refresh_table()

        # ==========================
        # THÔNG BÁO KẾT QUẢ
        # ==========================

        messagebox.showinfo(

            "Data Cleaning",

            f"""
Làm sạch dữ liệu thành công!

Số dòng ban đầu: {original_rows}

Số dòng hiện tại: {len(df)}

Đã xử lý:

- Xóa {duplicate_count} dòng trùng lặp

- Xóa {missing_title} dòng thiếu Title

- Điền Unknown cho:

  + Developer: {developer_null}

  + Publisher: {publisher_null}

  + Genres: {genres_null}

- Chuẩn hóa User Score

- Chuẩn hóa User Ratings Count

- Chuẩn hóa Release Date

- Chuẩn hóa Product Rating
"""
        )

    except Exception as e:

        messagebox.showerror(
            "Lỗi",
            str(e)
        )
