import customtkinter as ctk
import pandas as pd
from tkinter import messagebox


CSV_PATH = r"D:/LapTrinhPython/DOAN/VideoGamesProject/dataset/all_video_games(cleaned)_full.csv"


# ======================================================
# CREATE GAME
# ======================================================

def create_game(parent, df, tree, refresh_table):

    win = ctk.CTkToplevel(parent)

    win.title("Create New Game")

    win.geometry("550x850")

    fields = [
        "Title",
        "Release Date",
        "Developer",
        "Publisher",
        "Genres",
        "Product Rating",
        "User Score",
        "User Ratings Count",
        "Platforms Info"
    ]

    entries = {}

    for field in fields:

        ctk.CTkLabel(
            win,
            text=field
        ).pack(pady=(5, 2))

        entry = ctk.CTkEntry(
            win,
            width=350
        )

        entry.pack(pady=(0, 5))

        entries[field] = entry

    multi_add = ctk.BooleanVar()

    ctk.CTkCheckBox(
        win,
        text="Tiếp tục thêm game sau khi lưu",
        variable=multi_add
    ).pack(pady=10)

    def save_game():

        try:

            title = entries["Title"].get().strip()

            release = entries["Release Date"].get().strip()

            developer = entries["Developer"].get().strip()

            publisher = entries["Publisher"].get().strip()

            genres = entries["Genres"].get().strip()

            product = entries["Product Rating"].get().strip()

            score = float(entries["User Score"].get())

            ratings = int(entries["User Ratings Count"].get())

            platform = entries["Platforms Info"].get().strip()

            if title == "":

                messagebox.showerror(
                    "Lỗi",
                    "Title không được để trống!"
                )

                return

            if score < 0 or score > 10:

                messagebox.showerror(
                    "Lỗi",
                    "User Score phải từ 0 đến 10!"
                )

                return

            current_df = pd.read_csv(CSV_PATH)

            new_row = {

                "Title": title,

                "Release Date": release,

                "Developer": developer,

                "Publisher": publisher,

                "Genres": genres,

                "Product Rating": product,

                "User Score": score,

                "User Ratings Count": ratings,

                "Platforms Info": platform

            }

            current_df.loc[len(current_df)] = new_row

            current_df.to_csv(
                CSV_PATH,
                index=False
            )

            refresh_table()

            messagebox.showinfo(
                "Thành công",
                "Thêm game thành công!"
            )

            if multi_add.get():

                for e in entries.values():

                    e.delete(0, "end")

                entries["Title"].focus()

            else:

                win.destroy()

        except Exception as e:

            messagebox.showerror(
                "Lỗi",
                str(e)
            )

    ctk.CTkButton(

        win,

        text="💾 Save Game",

        width=250,

        height=45,

        command=save_game

    ).pack(pady=20)


# ======================================================
# READ GAME
# ======================================================

def read_games(tree):

    try:

        df = pd.read_csv(CSV_PATH)

        tree.delete(*tree.get_children())

        for _, row in df.iterrows():

            tree.insert(
                "",
                "end",
                values=list(row)
            )

        messagebox.showinfo(
            "Thành công",
            f"Đã tải {len(df)} game!"
        )

    except Exception as e:

        messagebox.showerror(
            "Lỗi",
            str(e)
        )


# ======================================================
# UPDATE GAME
# ======================================================

def update_game(tree, refresh_table):

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "Thông báo",
            "Vui lòng chọn game!"
        )

        return

    values = tree.item(selected[0], "values")

    update_window = ctk.CTkToplevel(tree.master)

    update_window.title("Update Game")

    update_window.geometry("550x800")

    labels = [

        "Title",

        "Release Date",

        "Developer",

        "Publisher",

        "Genres",

        "Product Rating",

        "User Score",

        "User Ratings Count",

        "Platforms Info"

    ]

    entries = []

    for i, label in enumerate(labels):

        ctk.CTkLabel(

            update_window,

            text=label

        ).pack(pady=5)

        entry = ctk.CTkEntry(

            update_window,

            width=350

        )

        entry.pack()

        entry.insert(0, values[i])

        entries.append(entry)

    def save_update():

        try:

            df = pd.read_csv(CSV_PATH)

            old_title = values[0]

            idx = df[df["Title"] == old_title].index

            if len(idx) == 0:

                messagebox.showerror(

                    "Lỗi",

                    "Không tìm thấy game!"

                )

                return

            row = idx[0]

            user_score = float(entries[6].get())

            user_ratings = int(entries[7].get())

            if user_score < 0 or user_score > 10:

                messagebox.showerror(

                    "Lỗi",

                    "User Score phải từ 0 đến 10!"

                )

                return

            df.at[row, "Title"] = entries[0].get().strip()

            df.at[row, "Release Date"] = entries[1].get().strip()

            df.at[row, "Developer"] = entries[2].get().strip()

            df.at[row, "Publisher"] = entries[3].get().strip()

            df.at[row, "Genres"] = entries[4].get().strip()

            df.at[row, "Product Rating"] = entries[5].get().strip()

            df.at[row, "User Score"] = user_score

            df.at[row, "User Ratings Count"] = user_ratings

            df.at[row, "Platforms Info"] = entries[8].get().strip()

            df.to_csv(

                CSV_PATH,

                index=False

            )

            refresh_table()

            messagebox.showinfo(

                "Thành công",

                "Cập nhật thành công!"

            )

            update_window.destroy()

        except ValueError:

            messagebox.showerror(

                "Lỗi",

                "User Score và User Ratings Count phải là số!"

            )

        except Exception as e:

            messagebox.showerror(

                "Lỗi",

                str(e)

            )

    ctk.CTkButton(

        update_window,

        text="💾 Save Update",

        width=250,

        height=45,

        command=save_update

    ).pack(pady=20)


# ======================================================
# DELETE GAME
# ======================================================

def delete_game(tree, refresh_table):

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "Thông báo",
            "Vui lòng chọn game cần xóa!"
        )

        return

    selected_titles = []

    for item in selected:

        values = tree.item(
            item,
            "values"
        )

        selected_titles.append(
            values[0]
        )

    confirm = messagebox.askyesno(

        "Xác nhận",

        f"Bạn có chắc muốn xóa {len(selected_titles)} game?"
    )

    if not confirm:

        return

    try:

        df = pd.read_csv(CSV_PATH)

        df = df[
            ~df["Title"].isin(
                selected_titles
            )
        ]

        df.to_csv(
            CSV_PATH,
            index=False
        )

        refresh_table()

        messagebox.showinfo(

            "Thành công",

            f"Đã xóa {len(selected_titles)} game!"
        )

    except Exception as e:

        messagebox.showerror(
            "Lỗi",
            str(e)
        )
