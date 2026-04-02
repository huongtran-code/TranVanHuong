import math

def tinh_tong_2_so(a, b):
    return a + b

def tinh_tong_nhieu_so(*args):
    return sum(args)

def la_so_nguyen_to(n):
    if n < 2:
        return False
    # Chỉ cần kiểm tra các ước từ 2 đến căn bậc hai của n
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            return False
    return True

def tim_so_nguyen_to_trong_khoang(a, b):
    ket_qua = []
    # Lặp từ a đến b (nếu a < 2 thì bắt đầu từ 2 vì số nguyên tố nhỏ nhất là 2)
    for i in range(max(2, a), b + 1):
        if la_so_nguyen_to(i):
            ket_qua.append(i)
    return ket_qua

# 5. Viết hàm kiểm tra số hoàn hảo
def la_so_hoan_hao(n):
    if n < 2:
        return False
    tong_uoc = 1 
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            tong_uoc += i
            if i != n // i:
                tong_uoc += n // i
    return tong_uoc == n

def tim_so_hoan_hao_trong_khoang(a, b):
    ket_qua = []
    for i in range(max(2, a), b + 1):
        if la_so_hoan_hao(i):
            ket_qua.append(i)
    return ket_qua

def chuong_trinh_menu():
    while True:
        print("\n" + "="*40)
        print("         LUYỆN TẬP")
        print("="*40)
        print("1. Tính tổng 2 số")
        print("2. Tính tổng các số truyền vào")
        print("3. Kiểm tra một số nguyên tố")
        print("4. Tìm các số nguyên tố trong khoảng [a,b]")
        print("5. Kiểm tra số hoàn hảo")
        print("6. Tìm các số hoàn hảo trong khoảng [a,b]")
        print("0. Thoát chương trình")
        
        chon = input("Nhập số tương ứng với chức năng (0-6): ")
        
        if chon == '0':
            print("Đã thoát chương trình. Hẹn gặp lại!")
            break
            
        elif chon == '1':
            a = float(input("Nhập số thứ nhất: "))
            b = float(input("Nhập số thứ hai: "))
            print(f"=> Tổng 2 số là: {tinh_tong_2_so(a, b)}")
            
        elif chon == '2':
            chuoi_so = input("Nhập các số (cách nhau bằng khoảng trắng): ")
            danh_sach_so = [float(x) for x in chuoi_so.split()]
            print(f"=> Tổng các số là: {tinh_tong_nhieu_so(*danh_sach_so)}")
            
        elif chon == '3':
            n = int(input("Nhập số nguyên cần kiểm tra: "))
            if la_so_nguyen_to(n):
                print(f"=> {n} là số nguyên tố.")
            else:
                print(f"=> {n} không phải là số nguyên tố.")
                
        elif chon == '4':
            a = int(input("Nhập khoảng bắt đầu (a): "))
            b = int(input("Nhập khoảng kết thúc (b): "))
            primes = tim_so_nguyen_to_trong_khoang(a, b)
            print(f"=> Các số nguyên tố trong khoảng [{a}, {b}] là:\n{primes}")
            
        elif chon == '5':
            n = int(input("Nhập số nguyên cần kiểm tra: "))
            if la_so_hoan_hao(n):
                print(f"=> {n} là số hoàn hảo.")
            else:
                print(f"=> {n} không phải là số hoàn hảo.")
                
        elif chon == '6':
            a = int(input("Nhập khoảng bắt đầu (a): "))
            b = int(input("Nhập khoảng kết thúc (b): "))
            perfects = tim_so_hoan_hao_trong_khoang(a, b)
            print(f"=> Các số hoàn hảo trong khoảng [{a}, {b}] là:\n{perfects}")
            
        else:
            print("=> Lựa chọn không hợp lệ, vui lòng nhập số từ 0 đến 6!")

if __name__ == "__main__":
    chuong_trinh_menu()