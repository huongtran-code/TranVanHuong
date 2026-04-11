from math_utils import phanso, hinhhoc

def main():
    print("--- CHƯƠNG TRÌNH TÍNH TOÁN ---")

    # --- Nhập dữ liệu cho Phân số ---
    print("\n1. Tính cộng hai phân số:")
    try:
        t1 = int(input("Nhập tử số 1: "))
        m1 = int(input("Nhập mẫu số 1: "))
        t2 = int(input("Nhập tử số 2: "))
        m2 = int(input("Nhập mẫu số 2: "))
        
        ket_qua_ps = phanso.cong_phan_so(t1, m1, t2, m2)
        print(f" => Kết quả: {t1}/{m1} + {t2}/{m2} = {ket_qua_ps}")
    except ValueError:
        print("Lỗi: Bạn phải nhập vào một số nguyên!")

    # --- Nhập dữ liệu cho Hình học ---
    print("\n2. Tính diện tích hình tròn:")
    try:
        r = float(input("Nhập bán kính hình tròn: "))
        dt = hinhhoc.dien_tich_tron(r)
        print(f" => Diện tích hình tròn là: {dt:.2f}")
    except ValueError:
        print("Lỗi: Vui lòng nhập số thập phân hoặc số nguyên cho bán kính!")

if __name__ == "__main__":
    main()