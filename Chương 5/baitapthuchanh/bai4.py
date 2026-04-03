# Nhập và lưu thông tin
ten = input("Họ tên: ")
tuoi = input("Tuổi: ")
email = input("Email: ")
skype = input("Skype: ")
dia_chi = input("Địa chỉ: ")
noi_lam_viec = input("Nơi làm việc: ")

with open("setInfo.txt", "w", encoding="utf-8") as f:
    f.write(f"Họ tên: {ten}\n")
    f.write(f"Tuổi: {tuoi}\n")
    f.write(f"Email: {email}\n")
    f.write(f"Skype: {skype}\n")
    f.write(f"Địa chỉ: {dia_chi}\n")
    f.write(f"Nơi làm việc: {noi_lam_viec}\n")

print("Đã lưu thông tin vào file 'setInfo.txt'!")

# Đọc và hiển thị thông tin
print("\nThông tin từ file 'setInfo.txt':")
with open("setInfo.txt", "r", encoding="utf-8") as f:
    print(f.read())