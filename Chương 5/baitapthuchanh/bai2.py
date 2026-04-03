text = input("Nhập đoạn văn bản muốn ghi: ")

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Đã ghi vào file thành công!")

# Hiển thị lại nội dung vừa ghi
with open("output.txt", "r", encoding="utf-8") as f:
    print("Nội dung file:", f.read())