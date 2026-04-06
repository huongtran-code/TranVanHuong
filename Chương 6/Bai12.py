# Danh sách cho trước theo ví dụ của đề bài
danh_sach_chuoi = ['abc', 'xyz', 'aba', '1221', 'ii', 'ii2', '5yhy5']

def dem_chuoi_thoa_dieu_kien(danh_sach, do_dai_toi_thieu):
    dem = 0
    for chuoi in danh_sach:
        if len(chuoi) >= do_dai_toi_thieu and len(chuoi) > 0 and chuoi[0] == chuoi[-1]:
            dem += 1
    return dem

try:
    do_dai_input = int(input("Bài 12 - Nhập độ dài tối thiểu của chuỗi: "))
    
    so_luong = dem_chuoi_thoa_dieu_kien(danh_sach_chuoi, do_dai_input)
    print(f"-> Kết quả cho ra: {so_luong}")

except ValueError:
    print("-> Lỗi: Vui lòng nhập một số nguyên hợp lệ!")