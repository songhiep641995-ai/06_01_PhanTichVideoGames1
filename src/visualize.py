import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(
    style="darkgrid",
    palette="viridis"
)
import customtkinter as ctk

PATH = r"D:/LapTrinhPython/DOAN/VideoGamesProject/dataset/all_video_games(cleaned)_full.csv"

def visualization_window(parent):

    win = ctk.CTkToplevel(parent)

    win.title("Visualization")
    win.geometry("450x500")

    ctk.CTkLabel(
        win,
        text="Select Charts",
        font=("Arial",20,"bold")
    ).pack(pady=20)

    genres_var = ctk.BooleanVar()
    publisher_var = ctk.BooleanVar()
    developer_var = ctk.BooleanVar()
    score_var = ctk.BooleanVar()
    game_var = ctk.BooleanVar()
    release_var = ctk.BooleanVar()
    platform_var = ctk.BooleanVar()

    ctk.CTkCheckBox(
        win,
        text="Top 10 Genres",
        variable=genres_var
    ).pack(anchor="w", padx=30)

    ctk.CTkCheckBox(
        win,
        text="Top 10 Publishers",
        variable=publisher_var
    ).pack(anchor="w", padx=30)

    ctk.CTkCheckBox(
        win,
        text="Top 10 Developers",
        variable=developer_var
    ).pack(anchor="w", padx=30)

    ctk.CTkCheckBox(
        win,
        text="User Score Distribution",
        variable=score_var
    ).pack(anchor="w", padx=30)

    ctk.CTkCheckBox(
        win,
        text="Top Games By User Score",
        variable=game_var
    ).pack(anchor="w", padx=30)

    ctk.CTkCheckBox(
        win,
        text="Games Released By Year",
        variable=release_var
    ).pack(anchor="w", padx=30)

    ctk.CTkCheckBox(
        win,
        text="Platform Distribution",
        variable=platform_var
    ).pack(anchor="w", padx=30)

    def show_selected():

        if genres_var.get():
            chart_top_genres()

        if publisher_var.get():
            chart_top_publishers()

        if developer_var.get():
            chart_top_developers()

        if score_var.get():
            chart_score_distribution()

        if game_var.get():
            chart_top_games()

        if release_var.get():
            chart_release_year()

        if platform_var.get():
            chart_platform_distribution()

    ctk.CTkButton(
        win,
        text="📊 Show Charts",
        command=show_selected
    ).pack(pady=25)
# =====================================
# 1. TOP 10 GENRES
# =====================================
def chart_top_genres():

    df = pd.read_csv(PATH)

    top = df["Genres"].value_counts().head(10)

    plt.figure(figsize=(12,6))

    sns.barplot(
    x=top.index,
    y=top.values
    )

    plt.xticks(rotation=45)
    plt.title("Top 10 Genres")
    plt.xlabel("Genres")
    plt.ylabel("Number of Games")
    plt.tight_layout()
    plt.show()
# =====================================
# 2. TOP 10 PUBLISHERS
# =====================================
def chart_top_publishers():

    df = pd.read_csv(PATH)

    top = df["Publisher"].value_counts().head(10)

    plt.figure(figsize=(12,6))

    sns.barplot(
    x=top.index,
    y=top.values
    )

    plt.xticks(rotation=45)
    plt.title("Top 10 Publishers")
    plt.xlabel("Publisher")
    plt.ylabel("Games")
    plt.tight_layout()
    plt.show()

# =====================================
# 3. TOP 10 DEVELOPERS
# =====================================
def chart_top_developers():

    df = pd.read_csv(PATH)

    top = df["Developer"].value_counts().head(10)

    plt.figure(figsize=(12,6))

    sns.barplot(
    x=top.index,
    y=top.values
    )

    plt.xticks(rotation=45)
    plt.title("Top 10 Developers")
    plt.xlabel("Developer")
    plt.ylabel("Games")
    plt.tight_layout()
    plt.show()


# =====================================
# 4. USER SCORE DISTRIBUTION
# =====================================
def chart_score_distribution():

    df = pd.read_csv(PATH)

    plt.figure(figsize=(10,6))

    sns.histplot(
    df["User Score"].dropna(),
    bins=20,
    kde=True
    )

    plt.title("User Score Distribution")
    plt.xlabel("User Score")
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()


# =====================================
# 5. TOP 10 GAMES BY USER SCORE
# =====================================
def chart_top_games():

    df = pd.read_csv(PATH)

    top = df.sort_values(
        by="User Score",
        ascending=False
    ).head(10)

    plt.figure(figsize=(12,6))

    sns.barplot(
    x="User Score",
    y="Title",
    data=top
    )

    plt.title("Top 10 Games By User Score")
    plt.tight_layout()
    plt.show()


# =====================================
# 6. GAMES RELEASED BY YEAR
# =====================================
def chart_release_year():

    df = pd.read_csv(PATH)

    df["Release Date"] = pd.to_datetime(
        df["Release Date"],
        errors="coerce"
    )

    df["Year"] = df["Release Date"].dt.year

    yearly = df["Year"].value_counts().sort_index()

    plt.figure(figsize=(12,6))

    sns.lineplot(
    x=yearly.index,
    y=yearly.values,
    marker="o"
    )

    plt.title("Games Released By Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Games")

    plt.tight_layout()
    plt.show()


# =====================================
# 7. PLATFORM DISTRIBUTION
# =====================================
def chart_platform_distribution():

    df = pd.read_csv(PATH)

    platform_count = {}

    for platforms in df["Platforms Info"].dropna():

        for p in str(platforms).split(","):

            p = p.strip()

            if p not in platform_count:
                platform_count[p] = 0

            platform_count[p] += 1

    platform_df = pd.Series(
        platform_count
    ).sort_values(
        ascending=False
    ).head(10)

    plt.figure(figsize=(8,8))

    plt.pie(
        platform_df,
        labels=platform_df.index,
        autopct="%1.1f%%",
        startangle=90,
        explode=[0.05] * len(platform_df),
        shadow=True
    )

    plt.title("Top 10 Platforms Distribution")

    plt.tight_layout()
    plt.show()
def show_chart(chart_name):

    if chart_name == "genres":
        chart_top_genres()

    elif chart_name == "publishers":
        chart_top_publishers()

    elif chart_name == "developers":
        chart_top_developers()

    elif chart_name == "score":
        chart_score_distribution()

    elif chart_name == "topgames":
        chart_top_games()

    elif chart_name == "release":
        chart_release_year()

    elif chart_name == "platform":
        chart_platform_distribution()
