import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# ============================================================
#  BƯỚC 4 — TRỰC QUAN HÓA DỮ LIỆU
#  Dataset: all_video_games_cleaned.csv
#  5 biểu đồ: Bar / Histogram / Pie / Line / Horizontal Bar
# ============================================================

# Cài đặt font chung cho tất cả biểu đồ
plt.rcParams['figure.facecolor'] = '#F8F9FA'
plt.rcParams['axes.facecolor']   = '#FFFFFF'
plt.rcParams['axes.grid']        = True
plt.rcParams['grid.alpha']       = 0.3
plt.rcParams['font.size']        = 11


def prepare_data(df):
    """
    Chuẩn bị dữ liệu trước khi vẽ.
    Tương thích cả 2 trường hợp:
      - Dùng file gốc (all_video_games_cleaned.csv)
      - Dùng file đã clean từ bước 2 (all_video_games_final.csv)
    """
    df = df.drop_duplicates().dropna(subset=['Title'])
    df['User Score']         = pd.to_numeric(df['User Score'], errors='coerce')
    df['User Ratings Count'] = pd.to_numeric(df['User Ratings Count'], errors='coerce')
    df['Release Date']       = pd.to_datetime(df['Release Date'], errors='coerce')

    # Chỉ map nếu cột chưa được rút gọn (tránh map() 2 lần → ra NaN)
    rating_map = {
        'Rated E For Everyone'        : 'E',
        'Rated T For Teen'            : 'T',
        'Rated M For Mature'          : 'M',
        'Rated E +10 For Everyone +10': 'E10+',
        'Rated RP For Rate Pending'   : 'RP',
        'Rated AO For Adults Only'    : 'AO',
    }
    already_mapped = df['Product Rating'].dropna().isin(['E', 'T', 'M', 'E10+', 'RP', 'AO']).all()
    if not already_mapped:
        df['Product Rating'] = df['Product Rating'].map(rating_map)

    df['Developer'] = df['Developer'].fillna('Unknown')
    df['Publisher']  = df['Publisher'].fillna('Unknown')
    df['Year']       = df['Release Date'].dt.year
    return df


# ------------------------------------------------------------
#  BIỂU ĐỒ 1 — Bar Chart: Top 10 Publisher nhiều game nhất
# ------------------------------------------------------------
def chart_top_publishers(df):
    top_pub = df['Publisher'].value_counts().head(10).sort_values()

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(top_pub.index, top_pub.values,
                   color='#4C72B0', edgecolor='white', linewidth=0.5)

    # Hiện số liệu trên mỗi thanh
    for bar in bars:
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                str(int(bar.get_width())),
                va='center', fontsize=10, color='#333333')

    ax.set_title('Top 10 Publisher có nhiều game nhất', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Số lượng game', fontsize=11)
    ax.set_xlim(0, top_pub.max() + 80)
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    plt.savefig('reports/chart1_top_publishers.png', dpi=150)
    plt.show()
    print("[✓] Biểu đồ 1 đã lưu: reports/chart1_top_publishers.png")


# ------------------------------------------------------------
#  BIỂU ĐỒ 2 — Histogram: Phân phối User Score
# ------------------------------------------------------------
def chart_user_score_distribution(df):
    scores = df['User Score'].dropna()

    fig, ax = plt.subplots(figsize=(10, 6))
    n, bins, patches = ax.hist(scores, bins=30, color='#55A868',
                                edgecolor='white', linewidth=0.5)

    # Đường trung bình
    mean_score = scores.mean()
    ax.axvline(mean_score, color='#C44E52', linestyle='--', linewidth=1.8,
               label=f'Trung bình: {mean_score:.2f}')

    ax.set_title('Phân phối User Score', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('User Score', fontsize=11)
    ax.set_ylabel('Số lượng game', fontsize=11)
    ax.legend(fontsize=10)
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    plt.savefig('reports/chart2_user_score_dist.png', dpi=150)
    plt.show()
    print("[✓] Biểu đồ 2 đã lưu: reports/chart2_user_score_dist.png")


# ------------------------------------------------------------
#  BIỂU ĐỒ 3 — Pie Chart: Tỷ lệ Product Rating
# ------------------------------------------------------------
def chart_product_rating(df):
    rating_counts = df['Product Rating'].value_counts()

    colors = ['#4C72B0', '#55A868', '#C44E52', '#8172B2', '#CCB974', '#64B5CD']
    explode = [0.03] * len(rating_counts)

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        rating_counts.values,
        labels=rating_counts.index,
        autopct='%1.1f%%',
        colors=colors[:len(rating_counts)],
        explode=explode,
        startangle=140,
        textprops={'fontsize': 11}
    )
    for at in autotexts:
        at.set_fontweight('bold')

    ax.set_title('Tỷ lệ phân loại độ tuổi (Product Rating)', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('reports/chart3_product_rating.png', dpi=150)
    plt.show()
    print("[✓] Biểu đồ 3 đã lưu: reports/chart3_product_rating.png")


# ------------------------------------------------------------
#  BIỂU ĐỒ 4 — Line Chart: Số game phát hành theo năm
# ------------------------------------------------------------
def chart_games_per_year(df):
    year_counts = (df['Year']
                   .dropna()
                   .astype(int)
                   .value_counts()
                   .sort_index())
    # Giới hạn năm hợp lý
    year_counts = year_counts[(year_counts.index >= 1995) & (year_counts.index <= 2024)]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(year_counts.index, year_counts.values,
            color='#4C72B0', linewidth=2, marker='o', markersize=5)
    ax.fill_between(year_counts.index, year_counts.values,
                    alpha=0.15, color='#4C72B0')

    # Đánh dấu năm đỉnh cao nhất
    peak_year = year_counts.idxmax()
    peak_val  = year_counts.max()
    ax.annotate(f'Đỉnh: {peak_year}\n({peak_val} game)',
                xy=(peak_year, peak_val),
                xytext=(peak_year - 4, peak_val - 80),
                arrowprops=dict(arrowstyle='->', color='#C44E52'),
                fontsize=10, color='#C44E52')

    ax.set_title('Số lượng game phát hành theo năm', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Năm', fontsize=11)
    ax.set_ylabel('Số lượng game', fontsize=11)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(3))
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    plt.savefig('reports/chart4_games_per_year.png', dpi=150)
    plt.show()
    print("[✓] Biểu đồ 4 đã lưu: reports/chart4_games_per_year.png")


# ------------------------------------------------------------
#  BIỂU ĐỒ 5 — Horizontal Bar: Top 10 thể loại game
# ------------------------------------------------------------
def chart_top_genres(df):
    top_genres = df['Genres'].value_counts().head(10).sort_values()

    colors = plt.cm.Blues([i / 12 for i in range(3, 13)])
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(top_genres.index, top_genres.values,
                   color=colors, edgecolor='white', linewidth=0.5)

    for bar in bars:
        ax.text(bar.get_width() + 4, bar.get_y() + bar.get_height() / 2,
                str(int(bar.get_width())),
                va='center', fontsize=10, color='#333333')

    ax.set_title('Top 10 thể loại game phổ biến nhất', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Số lượng game', fontsize=11)
    ax.set_xlim(0, top_genres.max() + 80)
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    plt.savefig('reports/chart5_top_genres.png', dpi=150)
    plt.show()
    print("[✓] Biểu đồ 5 đã lưu: reports/chart5_top_genres.png")


# ============================================================
#  CHẠY THỬ TRỰC TIẾP — vẽ tất cả 5 biểu đồ
# ============================================================
if __name__ == "__main__":
    import os
    os.makedirs('reports', exist_ok=True)   # tạo thư mục reports nếu chưa có

    INPUT_PATH = 'dataset/all_video_games_final.csv'   # ← file đã clean ở bước 2
    df = pd.read_csv(INPUT_PATH)
    df = prepare_data(df)

    print("=" * 50)
    print("  VẼ 5 BIỂU ĐỒ TRỰC QUAN HÓA DỮ LIỆU")
    print("=" * 50)

    chart_top_publishers(df)
    chart_user_score_distribution(df)
    chart_product_rating(df)
    chart_games_per_year(df)
    chart_top_genres(df)

    print("\n[✓] Hoàn tất! 5 ảnh PNG đã lưu vào thư mục reports/")