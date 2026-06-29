import customtkinter as ctk
import pandas as pd
from tkinter import messagebox
# ==========================
# SORT GAME
# ==========================

def sort_games(tree, sort_column, ascending=True):

    try:

        path = r"D:/LapTrinhPython/DOAN/VideoGamesProject/dataset/all_video_games(cleaned)_full.csv"

        df = pd.read_csv(path)

        # Kiểm tra cột
        if sort_column not in df.columns:

            messagebox.showerror(
                "Lỗi",
                f"Không tồn tại cột {sort_column}"
            )

            return

        # Sắp xếp
        df_sorted = df.sort_values(
            by=sort_column,
            ascending=ascending
        )

        # Xóa dữ liệu cũ
        tree.delete(*tree.get_children())

        # Hiển thị dữ liệu mới
        for _, row in df_sorted.iterrows():

            tree.insert(
                "",
                "end",
                values=list(row)
            )

        order = "Tăng dần" if ascending else "Giảm dần"

        messagebox.showinfo(
            "Thành công",
            f"Đã sắp xếp theo {sort_column}\n({order})"
        )

    except Exception as e:

        messagebox.showerror(
            "Lỗi",
            str(e)
        )
