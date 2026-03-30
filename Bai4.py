# Bài 4: Kiểm tra số nguyên dương chia hết cho 2, 3
try:
    n = int(input("Nhập một số nguyên dương: "))
    if n <= 0:
        print("Vui lòng nhập số nguyên dương!")
    else:
        if n % 2 == 0 and n % 3 == 0:
            print(f"Số {n} chia hết cho cả 2 và 3.")
        elif n % 2 == 0:
            print(f"Số {n} chia hết cho 2.")
        elif n % 3 == 0:
            print(f"Số {n} chia hết cho 3.")
        else:
            print(f"Số {n} không chia hết cho 2 và 3.")
except ValueError:
    print("Vui lòng nhập một số hợp lệ!")
