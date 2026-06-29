import customtkinter as ctk
import pandas as pd
from tkinter import ttk
from src.crud import create_game, read_games, update_game, delete_game
from src.search import search_game
from src.sort import sort_games
from src.clean_data import clean_data
from src.visualize import visualization_window
# ==========================
# APP SETTINGS
# ==========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv("D:/LapTrinhPython/DOAN/VideoGamesProject/dataset/all_video_games(cleaned)_full.csv")
# ==========================
# PAGINATION
# ==========================

ITEMS_PER_PAGE = 50

current_page = 1

total_records = len(df)

total_pages = (total_records + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
# ==========================
# REFRESH TABLE
# ==========================
def refresh_table():

    global df
    global current_page

    df = pd.read_csv(
        "D:/LapTrinhPython/DOAN/VideoGamesProject/dataset/all_video_games(cleaned)_full.csv"
    )

    total_pages = (
        len(df) + ITEMS_PER_PAGE - 1
    ) // ITEMS_PER_PAGE

    if current_page > total_pages:

        current_page = total_pages

    if current_page < 1:

        current_page = 1

    load_page(current_page)

    refresh_kpi()
def refresh_kpi():

    global df

    kpi_labels[0].configure(
        text=str(len(df))
    )

    kpi_labels[1].configure(
        text=str(df["Publisher"].nunique())
    )

    kpi_labels[2].configure(
        text=str(df["Developer"].nunique())
    )

    kpi_labels[3].configure(
        text=str(
            round(
                df["User Score"].mean(),
                2
            )
        )
    )
# ==========================
# PAGINATION FUNCTIONS
# ==========================

def load_page(page):

    global current_page

    current_page = page

    tree.delete(*tree.get_children())

    start = (page - 1) * ITEMS_PER_PAGE

    end = start + ITEMS_PER_PAGE

    page_data = df.iloc[start:end]

    for _, row in page_data.iterrows():

        tree.insert(
            "",
            "end",
            values=list(row)
        )

    update_pagination_label()


def update_pagination_label():

    total_records = len(df)

    total_pages = (
        total_records + ITEMS_PER_PAGE - 1
    ) // ITEMS_PER_PAGE

    start = (current_page - 1) * ITEMS_PER_PAGE + 1

    end = min(
        current_page * ITEMS_PER_PAGE,
        total_records
    )

    page_label.configure(
        text=f"Trang {current_page} / {total_pages}"
    )

    info_label.configure(
        text=f"Hiển thị {start} - {end} / {total_records:,} game"
    )


def first_page():

    load_page(1)


def previous_page():

    if current_page > 1:

        load_page(current_page - 1)


def next_page():

    total_pages = (
        len(df) + ITEMS_PER_PAGE - 1
    ) // ITEMS_PER_PAGE

    if current_page < total_pages:

        load_page(current_page + 1)


def last_page():

    total_pages = (
        len(df) + ITEMS_PER_PAGE - 1
    ) // ITEMS_PER_PAGE

    load_page(total_pages)


def go_to_page():

    try:

        page = int(page_entry.get())

        total_pages = (
            len(df) + ITEMS_PER_PAGE - 1
        ) // ITEMS_PER_PAGE

        if 1 <= page <= total_pages:

            load_page(page)

    except:

        pass
# ==========================
# WINDOW
# ==========================

app = ctk.CTk()
app.configure(
    fg_color="#1E1E2E"
)
app.title("Video Games Dashboard")
app.geometry("1600x900")

# ==========================
# SIDEBAR
# ==========================

sidebar = ctk.CTkFrame(
    app,
    width=260,
    corner_radius=0,
    fg_color="#181825"
)

sidebar.pack(
    side="left",
    fill="y"
)

logo = ctk.CTkLabel(
    sidebar,
    text="🎮 VIDEO GAMES\nDATA ANALYSIS",
    font=("Segoe UI", 26, "bold"),
    text_color="#FFFFFF"
)

logo.pack(pady=30)

dashboard_btn = ctk.CTkButton(
    sidebar,
    text="🏠 Dashboard",
    height=40,
    corner_radius=12
)

dashboard_btn.pack(
    fill="x",
    padx=10,
    pady=5
)

create_btn = ctk.CTkButton(
    sidebar,
    text="➕ Create",
    height=40,
    corner_radius=12
)

create_btn.pack(
    fill="x",
    padx=10,
    pady=5
)

read_btn = ctk.CTkButton(
    sidebar,
    text="📖 Read",
    height=40,
    corner_radius=12
)

read_btn.pack(
    fill="x",
    padx=10,
    pady=5
)

update_btn = ctk.CTkButton(
    sidebar,
    text="✏️ Update",
    height=40,
    corner_radius=12
)

update_btn.pack(
    fill="x",
    padx=10,
    pady=5
)

delete_btn = ctk.CTkButton(
    sidebar,
    text="🗑 Delete",
    height=40,
    corner_radius=12
)

delete_btn.pack(
    fill="x",
    padx=10,
    pady=5
)

search_btn = ctk.CTkButton(
    sidebar,
    text="🔍 Search",
    height=40,
    corner_radius=12
)

search_btn.pack(
    fill="x",
    padx=10,
    pady=5
)

sort_btn = ctk.CTkButton(
    sidebar,
    text="📊 Sort",
    height=40,
    corner_radius=12
)

sort_btn.pack(
    fill="x",
    padx=10,
    pady=5
)

visual_btn = ctk.CTkButton(
    sidebar,
    text="📈 Visualization",
    command=lambda: visualization_window(app),
    height=40,
    corner_radius=12
)
visual_btn.pack(
    fill="x",
    padx=10,
    pady=5
)
clean_btn = ctk.CTkButton(
    sidebar,
    text="🧹 Data Cleaning",
    height=40,
    corner_radius=12
)

clean_btn.pack(
    fill="x",
    padx=10,
    pady=5
)
# ==========================
# MAIN CONTENT
# ==========================

main = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

main.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# ==========================
# HEADER
# ==========================

header = ctk.CTkFrame(main)

header.pack(fill="x")

title = ctk.CTkLabel(
    header,
    text="🎮 Video Games Dashboard",
    font=("Segoe UI", 30, "bold")
)

title.pack(
    side="left",
    padx=20,
    pady=15
)

search_entry = ctk.CTkEntry(
    header,
    width=350,
    height=40,
    corner_radius=15,
    placeholder_text="🔍 Search games..."
)

search_entry.pack(
    side="right",
    padx=20
)
# ==========================
# SORT OPTIONS
# ==========================

sort_frame = ctk.CTkFrame(
    header,
    fg_color="transparent"
)

sort_frame.pack(
    side="right",
    padx=20
)

sort_column = ctk.StringVar(
    value="Title"
)

sort_order = ctk.StringVar(
    value="Ascending"
)

sort_menu = ctk.CTkOptionMenu(
    sort_frame,
    variable=sort_column,
    values=[
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
)

sort_menu.pack(
    side="left",
    padx=5
)

order_menu = ctk.CTkOptionMenu(
    sort_frame,
    variable=sort_order,
    values=[
        "Ascending",
        "Descending"
    ]
)

order_menu.pack(
    side="left",
    padx=5
)
# ==========================
# KPI CARDS
# ==========================

card_frame = ctk.CTkFrame(
    main,
    fg_color="transparent"
)

card_frame.pack(fill="x", pady=20)

cards = [
    ("🎮 Total Games", len(df)),
    ("🏢 Publishers", df["Publisher"].nunique()),
    ("💻 Developers", df["Developer"].nunique()),
    ("⭐ Avg Score", round(df["User Score"].mean(), 2))
]

# Lưu các label KPI để cập nhật sau này
kpi_labels = []

for title_card, value in cards:

    card = ctk.CTkFrame(
        card_frame,
        width=260,
        height=130,
        corner_radius=15,
        fg_color="#313244",
        border_width=1,
        border_color="#89B4FA"
    )

    card.pack(
        side="left",
        padx=10
    )

    card.pack_propagate(False)

    ctk.CTkLabel(
        card,
        text=title_card,
        font=("Segoe UI", 16)
    ).pack(pady=10)

    value_label = ctk.CTkLabel(
        card,
        text=str(value),
        font=("Segoe UI", 28, "bold")
    )

    value_label.pack()

    kpi_labels.append(value_label)
# ==========================
# TABLE
# ==========================

table_frame = ctk.CTkFrame(main)

table_frame.pack(
    fill="both",
    expand=True
)

columns = list(df.columns)
style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background="#313244",
    foreground="white",
    fieldbackground="#313244",
    rowheight=28,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background="#89B4FA",
    foreground="black",
    font=("Segoe UI", 10, "bold")
)

style.map(
    "Treeview",
    background=[("selected", "#74C7EC")]
)
tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="extended"
)

for col in columns:

    tree.heading(col,text=col)
    tree.column(col,width=130)

tree.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)
pagination_frame = ctk.CTkFrame(
    main,
    height=100
)

pagination_frame.pack(
    fill="x",
    pady=10
)

nav_frame = ctk.CTkFrame(
    pagination_frame,
    fg_color="transparent"
)

nav_frame.pack(
    pady=5
)

first_btn = ctk.CTkButton(
    nav_frame,
    text="<<",
    width=50,
    command=first_page
)

first_btn.pack(
    side="left",
    padx=5
)

prev_btn = ctk.CTkButton(
    nav_frame,
    text="< Previous",
    width=110,
    command=previous_page
)

prev_btn.pack(
    side="left",
    padx=5
)

page_label = ctk.CTkLabel(
    nav_frame,
    text=""
)

page_label.pack(
    side="left",
    padx=20
)

next_btn = ctk.CTkButton(
    nav_frame,
    text="Next >",
    width=110,
    command=next_page
)

next_btn.pack(
    side="left",
    padx=5
)

last_btn = ctk.CTkButton(
    nav_frame,
    text=">>",
    width=50,
    command=last_page
)

last_btn.pack(
    side="left",
    padx=5
)

info_label = ctk.CTkLabel(
    pagination_frame,
    text=""
)

info_label.pack(
    pady=5
)

goto_frame = ctk.CTkFrame(
    pagination_frame,
    fg_color="transparent"
)

goto_frame.pack()

ctk.CTkLabel(
    goto_frame,
    text="Go to page:"
).pack(
    side="left",
    padx=5
)

page_entry = ctk.CTkEntry(
    goto_frame,
    width=80
)

page_entry.pack(
    side="left",
    padx=5
)

go_btn = ctk.CTkButton(
    goto_frame,
    text="GO",
    width=70,
    command=go_to_page
)

go_btn.pack(
    side="left",
    padx=5
)
scroll_y = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)

tree.configure(
    yscrollcommand=scroll_y.set
)

scroll_y.pack(
    side="right",
    fill="y"
)
create_btn.configure(
    command=lambda:
    create_game(
        app,
        df,
        tree,
        refresh_table
    )
)
read_btn.configure(
    command=lambda:
    read_games(tree)
)
update_btn.configure(
    command=lambda:
    update_game(
        tree,
        refresh_table
    )
)
delete_btn.configure(
    command=lambda:
    delete_game(
        tree,
        refresh_table
    )
)
search_btn.configure(
    command=lambda:
    search_game(
        search_entry.get(),
        tree
    )
)
sort_btn.configure(
    command=lambda:
    sort_games(
        tree,
        sort_column.get(),
        True if sort_order.get() == "Ascending" else False
    )
)
from tkinter import messagebox

clean_btn.configure(

    command=lambda:

    clean_data(refresh_table)

    if messagebox.askyesno(
        "Data Cleaning",
        "Bạn có muốn làm sạch dữ liệu không?"
    )

    else None
)
load_page(1)
app.mainloop()
