# Tạo file demo_file2.txt
with open("demo_file2.txt", "w", encoding="utf-8") as f:
    f.write("Dem so luong tu xuat hien abc abc abc 12 12 it it eaut")

# Đọc và đếm số lần xuất hiện của từng từ
word_count = {}

with open("demo_file2.txt", "r", encoding="utf-8") as f:
    for line in f:
        words = line.split()
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1

print("Kết quả:", word_count)