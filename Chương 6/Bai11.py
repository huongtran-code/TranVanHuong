# Danh sách cho trước (bạn có thể tùy chỉnh danh sách này)
danh_sach_tu = ["python", "java", "c", "c++", "javascript", "ruby", "php"]

try:
    n = int(input("Nhập vào số nguyên n: "))
    
    ket_qua = [tu for tu in danh_sach_tu if len(tu) > n]
    
    print(f"-> Các từ có độ dài lớn hơn {n} trong danh sách là: {ket_qua}")

except ValueError:
    print("-> Lỗi: Vui lòng nhập một số nguyên hợp lệ!")