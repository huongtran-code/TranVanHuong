# Bài 5: Giải phương trình bậc 2
import math

try:
    a = float(input("Nhập hệ số a: "))
    b = float(input("Nhập hệ số b: "))
    c = float(input("Nhập hệ số c: "))

    if a == 0:
        if b == 0:
            print("Phương trình vô số nghiệm" if c == 0 else "Phương trình vô nghiệm")
        else:
            print(f"Phương trình có nghiệm x = {-c/b}")
    else:
        delta = b**2 - 4*a*c
        if delta < 0:
            print("Phương trình vô nghiệm.")
        elif delta == 0:
            print(f"Phương trình có nghiệm kép x1 = x2 = {-b/(2*a)}")
        else:
            _sqrt_delta = math.sqrt(delta) # Sử dụng math.sqrt() như gợi ý
            x1 = (-b + _sqrt_delta) / (2*a)
            x2 = (-b - _sqrt_delta) / (2*a)
            print(f"Phương trình có 2 nghiệm phân biệt: x1 = {x1}, x2 = {x2}")
except ValueError:
    print("Vui lòng nhập số hợp lệ!")
