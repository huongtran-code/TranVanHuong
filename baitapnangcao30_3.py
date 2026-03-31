import os
import subprocess

# 1. Nội dung giải Bài 4
bai4_code = """# Bài 4: Kiểm tra số nguyên dương chia hết cho 2, 3
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
"""

# 2. Nội dung giải Bài 5 (Phương trình bậc 2: a*x*x + b*x + c = 0)
bai5_code = """# Bài 5: Giải phương trình bậc 2
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
"""

def create_files():
    print("Đang tạo file Bai4.py và Bai5.py...")
    with open("Bai4.py", "w", encoding="utf-8") as f:
        f.write(bai4_code)
    with open("Bai5.py", "w", encoding="utf-8") as f:
        f.write(bai5_code)
    print("Đã tạo file thành công!")

def push_to_github(repo_url):
    print("Đang cấu hình Git và đẩy code lên GitHub...")
    commands = [
        ["git", "init"],
        ["git", "add", "."],
        ["git", "commit", "-m", "Hoàn thành Bài 4 và Bài 5"],
        ["git", "branch", "-M", "main"],
        ["git", "remote", "add", "origin", repo_url],
        ["git", "push", "-u", "origin", "main"]
    ]
    
    for cmd in commands:
        try:
            # Chạy từng lệnh Git
            subprocess.run(cmd, check=True, text=True, capture_output=True)
            print(f"Chạy thành công: {' '.join(cmd)}")
        except subprocess.CalledProcessError as e:
            # Xử lý riêng lỗi remote add origin nếu remote đã tồn tại
            if cmd[1] == "remote" and "already exists" in e.stderr:
                print("Remote origin đã tồn tại, tiếp tục lệnh push...")
            else:
                print(f"Lỗi khi chạy lệnh {' '.join(cmd)}: {e.stderr}")
                return
    print("Đã đẩy code lên GitHub thành công! 🎉")

if __name__ == "__main__":
    GITHUB_REPO = "https://github.com/huongtran-code/Python_test"
    
    create_files()
    push_to_github(GITHUB_REPO)