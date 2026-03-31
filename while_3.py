n = int(input("Nhập vào số nguyên dương n: "))

# Số nguyên tố phải lớn hơn 1
if n < 2:
    print("Không phải số nguyên tố.")
else:
    i = 2
    la_nguyen_to = True
    
    # Kiểm tra từ 2 đến căn bậc hai của n để tối ưu
    while i * i <= n:
        if n % i == 0:
            la_nguyen_to = False
            break  
        i += 1
        
    if la_nguyen_to:
        print("Đây là số nguyên tố.")
    else:
        print("Không phải số nguyên tố.")