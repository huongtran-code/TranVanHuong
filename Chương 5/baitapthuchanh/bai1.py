n = int(input("Nhập số dòng muốn đọc: "))

with open("demo_file1.txt", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i >= n:
            break
        print(line, end="")