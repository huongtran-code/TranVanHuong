
print("--- Bài 1 ---")
a1 = int(input("Nhập số nguyên thứ nhất: "))
b1 = int(input("Nhập số nguyên thứ hai: "))
print(f"Tổng của hai số là: {a1 + b1}")

print("\n--- Bài 2 ---")
chuoi = input("Nhập vào một chuỗi ký tự: ")
print(f"Chuỗi bạn vừa nhập là: {chuoi}")

print("\n--- Bài 3 ---")
x = int(input("Nhập số thứ nhất: "))
y = int(input("Nhập số thứ hai: "))
z = int(input("Nhập số thứ ba: "))

# a) Tổng và tích
print(f"a) Tổng: {x + y + z}, Tích: {x * y * z}")

# b) Hiệu của 2 số bất kỳ (ví dụ x và y)
print(f"b) Hiệu của {x} và {y} là: {x - y}")

# c) Chia lấy nguyên, dư và kết quả chính xác của 2 số bất kỳ (ví dụ x và y)
if y != 0:
    print(f"c) Chia lấy nguyên: {x // y}")
    print(f"   Chia lấy dư: {x % y}")
    print(f"   Kết quả chính xác: {x / y}")
else:
    print("c) Không thể chia cho 0")

print("\n--- Bài 4 ---")
ho = input("Nhập chuỗi 1 (Họ): ")
dem = input("Nhập chuỗi 2 (Tên đệm): ")
ten = input("Nhập chuỗi 3 (Tên): ")
# Ghép chuỗi dùng dấu cách ở giữa
ho_ten = ho + " " + dem + " " + ten
print(f"Kết quả ghép chuỗi: '{ho_ten}'")

print("\n--- Bài 5 ---")
_R = float(input("Nhập bán kính đường tròn (R): "))
_pi = 3.14

CV = 2 * _R * _pi
DT = _pi * _R * _R

print(f"Chu vi hình tròn là: {CV}")
print(f"Diện tích hình tròn là: {DT}")