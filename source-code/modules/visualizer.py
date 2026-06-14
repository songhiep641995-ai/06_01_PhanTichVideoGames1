import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# ============================================================
#  BƯỚC 4 — TRỰC QUAN HÓA DỮ LIỆU
#  5 biểu đồ sử dụng các cột kể cả cột mới từ Feature Engineering
# ============================================================

plt.rcParams['figure.facecolor'] = '#F8F9FA'
plt.rcParams['axes.facecolor']   = '#FFFFFF'
plt.rcParams['axes.grid']        = True
plt.rcParams['grid.alpha']       = 0.3
plt.rcParams['font.size']        = 11


def prepare_data(df):
    """
    Tương thích file gốc hoặc file đã qua data_cleaner.
    Đảm bảo các cột cần thiết đều tồn tại.
    """
    df = df.drop_duplicates(subset=['Title']).dropna(subset=['Title'])
    df['User Score']         = pd.to_numeric(df['User Score'], errors='coerce')
    df['User Ratings Count'] = pd.to_numeric(df['User Ratings Count'], errors='coerce')
    df['Release Date']       = pd.to_datetime(df['Release Date'], errors='coerce')
    df['Developer']          = df['Developer'].fillna('Unknown')
    df['Publisher']          = df['Publisher'].fillna('Unknown')
    df['Product Rating']     = df['Product Rating'].fillna('Not Rated')

    # Median fillna
    df['User Score']         = df['User Score'].fillna(df['User Score'].median())
    df['User Ratings Count'] = df['User Ratings Count'].fillna(0)

    # Feature Engineering (nếu chưa có)
    if 'Release Year' not in df.columns:
        df['Release Year'] = df['Release Date'].dt.year
    if 'Game Age' not in df.columns:
        df['Game Age'] = 2025 - df['Release Year']
    if 'Score Category' not in df.columns:
        def phan_loai(s):
            if pd.isna(s): return 'Không rõ'
            if s < 6: return 'Thấp'
            if s <= 7.5: return 'Trung bình'
            return 'Cao'
        df['Score Category'] = df['User Score'].apply(phan_loai)

    return df


# Biểu đồ 1 — Top 10 Publisher
def chart_top_publishers(df):
    top_pub = df['Publisher'].value_counts().head(10).sort_values()
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(top_pub.index, top_pub.values, color='#4C72B0', edgecolor='white')
    for bar in bars:
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                str(int(bar.get_width())), va='center', fontsize=10)
    ax.set_title('Top 10 Publisher có nhiều game nhất', fontsize=14, fontweight='bold')
    ax.set_xlabel('Số lượng game')
    ax.set_xlim(0, top_pub.max() + 80)
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    plt.savefig('reports/chart1_top_publishers.png', dpi=150)
    plt.show()
    print("[✓] Biểu đồ 1 lưu: reports/chart1_top_publishers.png")


# Biểu đồ 2 — Histogram User Score
def chart_user_score_distribution(df):
    scores = df['User Score'].dropna()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(scores, bins=30, color='#55A868', edgecolor='white')
    mean_score = scores.mean()
    ax.axvline(mean_score, color='#C44E52', linestyle='--', linewidth=1.8,
               label=f'Trung bình: {mean_score:.2f}')
    ax.set_title('Phân phối User Score', fontsize=14, fontweight='bold')
    ax.set_xlabel('User Score')
    ax.set_ylabel('Số lượng game')
    ax.legend()
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    plt.savefig('reports/chart2_user_score_dist.png', dpi=150)
    plt.show()
    print("[✓] Biểu đồ 2 lưu: reports/chart2_user_score_dist.png")


# Biểu đồ 3 — Pie Chart Score Category (dùng cột Feature Engineering)
def chart_score_category(df):
    cat_counts = df['Score Category'].value_counts()
    colors = ['#55A868', '#4C72B0', '#C44E52', '#CCCCCC']
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        cat_counts.values, labels=cat_counts.index,
        autopct='%1.1f%%', colors=colors[:len(cat_counts)],
        explode=[0.03] * len(cat_counts), startangle=140,
        textprops={'fontsize': 12}
    )
    for at in autotexts:
        at.set_fontweight('bold')
    ax.set_title('Phân loại game theo Score Category', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('reports/chart3_score_category.png', dpi=150)
    plt.show()
    print("[✓] Biểu đồ 3 lưu: reports/chart3_score_category.png")


# Biểu đồ 4 — Line Chart số game theo năm
def chart_games_per_year(df):
    year_counts = (df['Release Year'].dropna().astype(int)
                   .value_counts().sort_index())
    year_counts = year_counts[(year_counts.index >= 1995) & (year_counts.index <= 2024)]
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(year_counts.index, year_counts.values,
            color='#4C72B0', linewidth=2, marker='o', markersize=5)
    ax.fill_between(year_counts.index, year_counts.values, alpha=0.15, color='#4C72B0')
    peak_year = year_counts.idxmax()
    peak_val  = year_counts.max()
    ax.annotate(f'Đỉnh: {peak_year}\n({peak_val} game)',
                xy=(peak_year, peak_val),
                xytext=(peak_year - 4, peak_val - 80),
                arrowprops=dict(arrowstyle='->', color='#C44E52'),
                fontsize=10, color='#C44E52')
    ax.set_title('Số lượng game phát hành theo năm (1995–2024)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Năm')
    ax.set_ylabel('Số lượng game')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(3))
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    plt.savefig('reports/chart4_games_per_year.png', dpi=150)
    plt.show()
    print("[✓] Biểu đồ 4 lưu: reports/chart4_games_per_year.png")


# Biểu đồ 5 — Top 10 thể loại
def chart_top_genres(df):
    top_genres = df['Genres'].value_counts().head(10).sort_values()
    colors = plt.cm.Blues([i / 12 for i in range(3, 13)])
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(top_genres.index, top_genres.values, color=colors, edgecolor='white')
    for bar in bars:
        ax.text(bar.get_width() + 4, bar.get_y() + bar.get_height() / 2,
                str(int(bar.get_width())), va='center', fontsize=10)
    ax.set_title('Top 10 thể loại game phổ biến nhất', fontsize=14, fontweight='bold')
    ax.set_xlabel('Số lượng game')
    ax.set_xlim(0, top_genres.max() + 80)
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    plt.savefig('reports/chart5_top_genres.png', dpi=150)
    plt.show()
    print("[✓] Biểu đồ 5 lưu: reports/chart5_top_genres.png")


# ============================================================
#  CHẠY THỬ
# ============================================================
if __name__ == "__main__":
    import os
    os.makedirs('reports', exist_ok=True)

    INPUT_PATH = 'dataset/all_video_games_final.csv'
    df = pd.read_csv(INPUT_PATH)
    df = prepare_data(df)

    print("=" * 50)
    print("  VẼ 5 BIỂU ĐỒ TRỰC QUAN HÓA")
    print("=" * 50)

    chart_top_publishers(df)
    chart_user_score_distribution(df)
    chart_score_category(df)
    chart_games_per_year(df)
    chart_top_genres(df)

    print("\n[✓] Hoàn tất! 5 ảnh PNG đã lưu vào thư mục reports/")
