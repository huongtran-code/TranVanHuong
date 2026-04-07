class HocVien:
    def __init__(self, ho_ten, ngay_sinh, email, dien_thoai, dia_chi, lop):
        self.ho_ten = ho_ten
        self.ngay_sinh = ngay_sinh
        self.email = email
        self.dien_thoai = dien_thoai
        self.dia_chi = dia_chi
        self.lop = lop

    def show_info(self):
        print("--- THÔNG TIN HỌC VIÊN ---")
        print(f"Họ tên: {self.ho_ten}")
        print(f"Ngày sinh: {self.ngay_sinh}")
        print(f"Email: {self.email}")
        print(f"Điện thoại: {self.dien_thoai}")
        print(f"Địa chỉ: {self.dia_chi}")
        print(f"Lớp: {self.lop}")
        print("-" * 26)

    def change_info(self, dia_chi="Hà Nội", lop="IT12.x"):
        self.dia_chi = dia_chi
        self.lop = lop
        print("[Thông báo] Đã cập nhật thông tin học viên!\n")


if __name__ == "__main__":
    hoc_vien_1 = HocVien(
        ho_ten="Nguyễn Văn A", 
        ngay_sinh="15/08/2002", 
        email="nva@gmail.com", 
        dien_thoai="0987654321", 
        dia_chi="Hải Phòng", 
        lop="IT11.A"
    )

    print("1. Gọi hàm show_info() lần đầu:")
    hoc_vien_1.show_info()

    print("2. Gọi hàm change_info() với tham số mặc định:")
    hoc_vien_1.change_info()
    
    print("3. Thông tin học viên sau khi cập nhật:")
    hoc_vien_1.show_info()
    
    print("4. Gọi hàm change_info() truyền vào tham số mới:")
    hoc_vien_1.change_info(dia_chi="Đà Nẵng", lop="IT14.B")
    hoc_vien_1.show_info()