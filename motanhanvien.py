class NhanVien:
    # lớp mô tả cho mọi nhân viên
    dem = 0

    def __init__(self, name, salary):
        self.__name = name
        self.__salary = salary
        NhanVien.dem += 1
        
    def hien_thi_so_luong(self):
        print(f"Số lượng nhân viên: %d" % NhanVien.dem)
        
    def hien_thi_thong_tin(self):
        print("Tên: ", self.__name, ", Lương: ", self.__salary)
        
    # Đã sửa 'delf' thành 'self'
    def cap_nhat(self, name=None, salary=None):
        if name is not None: 
            self.__name = name 
        if salary is not None:
            self.__salary = salary
            
    # Thêm hàm (getter) để hỗ trợ lấy thuộc tính private __name từ bên ngoài
    def get_name(self):
        return self.__name


nhan_vien_dev = NhanVien("Nguyen Van A", 1000)
nhan_vien_test = NhanVien("Nguyen Van B", 1200)

# Đã sửa lại đúng tên hàm định nghĩa trong class
nhan_vien_dev.hien_thi_thong_tin()
nhan_vien_test.hien_thi_thong_tin()

print(nhan_vien_dev.dem)

# Đã thay đổi cách lấy tên thông qua hàm getter do __name là biến private
print(nhan_vien_dev.get_name())
print(nhan_vien_test.get_name())