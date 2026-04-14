import sys
import os
import sqlite3
import re
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

# ==========================================
# 0. CẤU HÌNH ĐƯỜNG DẪN TỰ ĐỘNG (FIX LỖI PATH)
# ==========================================
# Lấy đường dẫn thư mục hiện tại chứa file main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Tạo đường dẫn đầy đủ đến các file UI và Database
UI_DANG_KY = os.path.join(BASE_DIR, "dang_ky.ui")
UI_DANH_SACH = os.path.join(BASE_DIR, "danh_sach.ui")
DB_PATH = os.path.join(BASE_DIR, "thanhvien.db")

# ==========================================
# 1. KHỞI TẠO DATABASE
# ==========================================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ho TEXT,
            ten TEXT,
            lien_he TEXT,
            mat_khau TEXT,
            ngay_sinh TEXT,
            gioi_tinh TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ==========================================
# 2. HÀM KIỂM TRA MẬT KHẨU (REGEX)
# ==========================================
def kiem_tra_mat_khau(mk):
    if len(mk) < 8: return False
    if not re.search(r"[a-z]", mk): return False
    if not re.search(r"[A-Z]", mk): return False
    if not re.search(r"[0-9]", mk): return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", mk): return False
    return True

# ==========================================
# 3. CLASS GIAO DIỆN ĐĂNG KÝ / CHỈNH SỬA
# ==========================================
class DangKyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent_window=None, edit_id=None):
        super().__init__()
        # Load UI bằng đường dẫn tuyệt đối đã cấu hình ở đầu file
        try:
            uic.loadUi(UI_DANG_KY, self)
        except Exception as e:
            print(f"Lỗi không tìm thấy file UI: {UI_DANG_KY}")
            return

        self.parent_window = parent_window
        self.edit_id = edit_id

        # Khởi tạo dữ liệu cho ComboBox
        self.cb_ngay.addItems([str(i) for i in range(1, 32)])
        self.cb_thang.addItems([str(i) for i in range(1, 13)])
        self.cb_nam.addItems([str(i) for i in range(1970, 2026)])

        self.btn_dangky.clicked.connect(self.xu_ly_luu_du_lieu)

        if self.edit_id:
            self.setWindowTitle("Cập nhật thông tin")
            self.btn_dangky.setText("Cập nhật")
            self.load_du_lieu_cu()

    def load_du_lieu_cu(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id=?", (self.edit_id,))
        row = c.fetchone()
        conn.close()

        if row:
            self.txt_ho.setText(row[1])
            self.txt_ten.setText(row[2])
            self.txt_lienhe.setText(row[3])
            self.txt_matkhau.setText(row[4])
            ngay, thang, nam = row[5].split('/')
            self.cb_ngay.setCurrentText(ngay)
            self.cb_thang.setCurrentText(thang)
            self.cb_nam.setCurrentText(nam)
            if row[6] == 'Nam': self.rad_nam.setChecked(True)
            else: self.rad_nu.setChecked(True)
            self.chk_dongy.setChecked(True)

    def xu_ly_luu_du_lieu(self):
        ho = self.txt_ho.text().strip()
        ten = self.txt_ten.text().strip()
        lien_he = self.txt_lienhe.text().strip()
        mat_khau = self.txt_matkhau.text().strip()
        ngay_sinh = f"{self.cb_ngay.currentText()}/{self.cb_thang.currentText()}/{self.cb_nam.currentText()}"
        gioi_tinh = "Nam" if self.rad_nam.isChecked() else "Nữ"

        if not all([ho, ten, lien_he, mat_khau]) or not (self.rad_nam.isChecked() or self.rad_nu.isChecked()):
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        if not self.chk_dongy.isChecked():
            QMessageBox.warning(self, "Lỗi", "Bạn phải đồng ý với điều khoản!")
            return

        if not kiem_tra_mat_khau(mat_khau):
            QMessageBox.warning(self, "Mật khẩu yếu", "Mật khẩu >= 8 ký tự, có Chữ Hoa, Thường, Số và Ký tự đặc biệt!")
            return

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        if self.edit_id:
            c.execute('''UPDATE users SET ho=?, ten=?, lien_he=?, mat_khau=?, ngay_sinh=?, gioi_tinh=? WHERE id=?''', 
                      (ho, ten, lien_he, mat_khau, ngay_sinh, gioi_tinh, self.edit_id))
        else:
            c.execute('''INSERT INTO users (ho, ten, lien_he, mat_khau, ngay_sinh, gioi_tinh) VALUES (?, ?, ?, ?, ?, ?)''', 
                      (ho, ten, lien_he, mat_khau, ngay_sinh, gioi_tinh))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Thành công", "Dữ liệu đã được lưu!")
        if self.parent_window: self.parent_window.load_data()
        self.close()

# ==========================================
# 4. CLASS GIAO DIỆN DANH SÁCH
# ==========================================
class DanhSachWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            uic.loadUi(UI_DANH_SACH, self)
        except Exception as e:
            print(f"Lỗi không tìm thấy file UI: {UI_DANH_SACH}")
            return

        self.load_data()
        self.btn_xoa.clicked.connect(self.xoa_thanh_vien)
        self.btn_sua.clicked.connect(self.sua_thanh_vien)
        self.btn_them.clicked.connect(self.them_thanh_vien)

    def load_data(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        conn.close()

        self.table_danhsach.setRowCount(0)
        for row_idx, row_data in enumerate(rows):
            self.table_danhsach.insertRow(row_idx)
            for col_idx, col_data in enumerate(row_data):
                self.table_danhsach.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def xoa_thanh_vien(self):
        row = self.table_danhsach.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Chọn một thành viên để xóa!")
            return
        
        user_id = self.table_danhsach.item(row, 0).text()
        reply = QMessageBox.question(self, 'Xác nhận', 'Bạn muốn xóa thành viên này?', 
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE id=?", (user_id,))
            conn.commit()
            conn.close()
            self.load_data()

    def sua_thanh_vien(self):
        row = self.table_danhsach.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Chọn một thành viên để sửa!")
            return
        
        user_id = self.table_danhsach.item(row, 0).text()
        self.edit_win = DangKyWindow(parent_window=self, edit_id=user_id)
        self.edit_win.show()

    def them_thanh_vien(self):
        self.reg_win = DangKyWindow(parent_window=self)
        self.reg_win.show()

# ==========================================
# 5. CHẠY ỨNG DỤNG
# ==========================================
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    init_db()
    main_win = DanhSachWindow()
    main_win.show()
    sys.exit(app.exec())