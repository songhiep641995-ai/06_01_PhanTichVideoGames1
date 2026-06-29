import customtkinter as ctk
import pandas as pd
from tkinter import messagebox
# ==========================
# SEARCH GAME
# ==========================

def search_game(keyword, tree):

    try:

        # Đọc dữ liệu CSV
        path = r"D:/LapTrinhPython/DOAN/VideoGamesProject/dataset/all_video_games(cleaned)_full.csv"

        df = pd.read_csv(path)

        # Kiểm tra từ khóa
        if keyword.strip() == "":

            messagebox.showwarning(
                "Thông báo",
                "Vui lòng nhập từ khóa tìm kiếm!"
            )

            return

        # Xóa dữ liệu cũ trên Treeview
        tree.delete(*tree.get_children())

        # Tìm kiếm theo Title
        result = df[
            df["Title"]
            .astype(str)
            .str.contains(
                keyword,
                case=False,
                na=False
            )
        ]

        # Không tìm thấy
        if result.empty:

            messagebox.showinfo(
                "Kết quả",
                "Không tìm thấy game!"
            )

            return

        # Hiển thị kết quả
        for _, row in result.iterrows():

            tree.insert(
                "",
                "end",
                values=list(row)
            )

        messagebox.showinfo(
            "Thành công",
            f"Tìm thấy {len(result)} game!"
        )

    except Exception as e:

        messagebox.showerror(
            "Lỗi",
            str(e)
        )

