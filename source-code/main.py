import pandas as pd
import os
import sys

# Thêm đường dẫn modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from data_reader   import load_data, describe_data
from data_cleaner  import (kiem_tra_du_lieu, lam_sach_du_lieu,
                            chuan_hoa_du_lieu, feature_engineering,
                            thong_ke_sau_xu_ly, save_clean_data)
from crud          import (create_record, read_all, read_by_title,
                            read_by_genre, read_by_score_category,
                            read_top_scores, update_record,
                            delete_record, save_data)
from visualizer    import (prepare_data, chart_top_publishers,
                            chart_user_score_distribution, chart_score_category,
                            chart_games_per_year, chart_top_genres)

# ============================================================
INPUT_PATH  = 'dataset/all_video_games_cleaned.csv'
CLEAN_PATH  = 'dataset/all_video_games_final.csv'
CRUD_PATH   = 'dataset/all_video_games_crud.csv'

df = None   # DataFrame toàn cục


def hien_thi_menu():
    print("\n" + "=" * 50)
    print("   HỆ THỐNG PHÂN TÍCH VIDEO GAMES")
    print("=" * 50)
    print("  1. Xem thông tin dataset")
    print("  2. Kiểm tra dữ liệu thiếu & trùng")
    print("  3. Làm sạch & chuẩn hóa dữ liệu")
    print("  4. Feature Engineering (tạo cột mới)")
    print("  ─────────────────────────────────")
    print("  5. Tìm kiếm game theo tên")
    print("  6. Tìm game theo thể loại")
    print("  7. Xem game theo Score Category")
    print("  8. Top 10 game điểm cao nhất")
    print("  9. Thêm game mới")
    print("  10. Sửa thông tin game")
    print("  11. Xóa game")
    print("  ─────────────────────────────────")
    print("  12. Vẽ tất cả biểu đồ")
    print("  0.  Thoát")
    print("=" * 50)
    return input("Chọn chức năng: ").strip()


def main():
    global df
    os.makedirs('reports', exist_ok=True)

    # Tải dữ liệu lúc khởi động
    if os.path.exists(CLEAN_PATH):
        df = pd.read_csv(CLEAN_PATH)
        print(f"[✓] Đã tải file đã xử lý: {CLEAN_PATH} ({len(df)} dòng)")
    else:
        df = load_data(INPUT_PATH)

    while True:
        chon = hien_thi_menu()

        if chon == '0':
            print("Thoát chương trình. Tạm biệt!")
            break

        elif chon == '1':
            describe_data(df)

        elif chon == '2':
            df_tmp = pd.read_csv(INPUT_PATH)
            kiem_tra_du_lieu(df_tmp)

        elif chon == '3':
            df_tmp = pd.read_csv(INPUT_PATH)
            df_tmp = lam_sach_du_lieu(df_tmp)
            df     = chuan_hoa_du_lieu(df_tmp)
            thong_ke_sau_xu_ly(df)
            save_clean_data(df, CLEAN_PATH)

        elif chon == '4':
            df = feature_engineering(df)
            save_clean_data(df, CLEAN_PATH)

        elif chon == '5':
            kw = input("Nhập từ khóa tên game: ").strip()
            read_by_title(df, kw)

        elif chon == '6':
            genre = input("Nhập thể loại (vd: RPG, Action, FPS): ").strip()
            read_by_genre(df, genre)

        elif chon == '7':
            print("Chọn: 1-Thấp  2-Trung bình  3-Cao")
            opt = input("Chọn: ").strip()
            cat = {'1': 'Thấp', '2': 'Trung bình', '3': 'Cao'}.get(opt, 'Cao')
            read_by_score_category(df, cat)

        elif chon == '8':
            read_top_scores(df, n=10)

        elif chon == '9':
            title    = input("Tên game: ").strip()
            dev      = input("Developer: ").strip()
            pub      = input("Publisher: ").strip()
            genre    = input("Genres: ").strip()
            score    = float(input("User Score (0-10): ").strip())
            df = create_record(df, title=title, developer=dev,
                               publisher=pub, genres=genre, user_score=score)
            save_data(df, CRUD_PATH)

        elif chon == '10':
            title  = input("Tên game cần sửa: ").strip()
            col    = input("Tên cột cần sửa: ").strip()
            val    = input("Giá trị mới: ").strip()
            df = update_record(df, title, col, val)
            save_data(df, CRUD_PATH)

        elif chon == '11':
            title = input("Tên game cần xóa: ").strip()
            df = delete_record(df, title)
            save_data(df, CRUD_PATH)

        elif chon == '12':
            df_viz = prepare_data(df.copy())
            chart_top_publishers(df_viz)
            chart_user_score_distribution(df_viz)
            chart_score_category(df_viz)
            chart_games_per_year(df_viz)
            chart_top_genres(df_viz)

        else:
            print("[!] Lựa chọn không hợp lệ. Vui lòng thử lại.")


if __name__ == "__main__":
    main()
