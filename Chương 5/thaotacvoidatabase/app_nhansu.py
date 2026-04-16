import sys
import sqlite3
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QFormLayout, QGroupBox, QLabel, QLineEdit, 
                             QDateEdit, QComboBox, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt5.QtCore import QDate

class QuanLyNhanSuApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phần Mềm Quản Lý Nhân Sự - SQLite")
        self.resize(900, 600)
        
        # --- THÊM 2 DÒNG NÀY ---
        # Lấy thư mục chứa file app_nhansu.py hiện tại
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Tạo đường dẫn tuyệt đối cho file nhansu.db
        self.db_path = os.path.join(base_dir, 'nhansu.db')

        self.create_db() # Khởi tạo Database
        self.setup_ui()  # Khởi tạo Giao diện
        self.load_data() # Tải dữ liệu lên bảng khi mở app

    # ================= 1. KHỞI TẠO CƠ SỞ DỮ LIỆU =================
    def create_db(self):
        # Kết nối tới database (nếu chưa có sẽ tự tạo file nhansu.db)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Tạo bảng NhanSu nếu chưa tồn tại
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS NhanSu (
                CCCD TEXT PRIMARY KEY,
                HoTen TEXT,
                NgaySinh TEXT,
                GioiTinh TEXT,
                DiaChi TEXT
            )
        ''')
        conn.commit()
        conn.close()

    # ================= 2. THIẾT KẾ GIAO DIỆN (UI) =================
    def setup_ui(self):
        main_layout = QVBoxLayout()

        # --- Form nhập thông tin ---
        group_info = QGroupBox("Thông Tin Nhân Sự")
        form_layout = QFormLayout()

        self.txt_cccd = QLineEdit()
        self.txt_hoten = QLineEdit()
        self.date_ngaysinh = QDateEdit()
        self.date_ngaysinh.setCalendarPopup(True)
        self.date_ngaysinh.setDate(QDate.currentDate())
        self.date_ngaysinh.setDisplayFormat("dd/MM/yyyy")
        
        self.cb_gioitinh = QComboBox()
        self.cb_gioitinh.addItems(["Nam", "Nữ", "Khác"])
        
        self.txt_diachi = QLineEdit()

        form_layout.addRow("Số CCCD (Khóa chính):", self.txt_cccd)
        form_layout.addRow("Họ và tên:", self.txt_hoten)
        form_layout.addRow("Ngày sinh:", self.date_ngaysinh)
        form_layout.addRow("Giới tính:", self.cb_gioitinh)
        form_layout.addRow("Địa chỉ thường trú:", self.txt_diachi)
        group_info.setLayout(form_layout)
        main_layout.addWidget(group_info)

        # --- Nút chức năng ---
        layout_buttons = QHBoxLayout()
        self.btn_them = QPushButton("Thêm mới")
        self.btn_sua = QPushButton("Sửa thông tin")
        self.btn_xoa = QPushButton("Xóa nhân sự")
        self.btn_hienthi = QPushButton("Hiển thị / Làm mới")
        
        layout_buttons.addWidget(self.btn_them)
        layout_buttons.addWidget(self.btn_sua)
        layout_buttons.addWidget(self.btn_xoa)
        layout_buttons.addWidget(self.btn_hienthi)
        main_layout.addLayout(layout_buttons)

        # --- Tìm kiếm ---
        group_search = QGroupBox("Tìm Kiếm")
        layout_search = QHBoxLayout()
        
        self.cb_timkiem_theo = QComboBox()
        self.cb_timkiem_theo.addItems(["Số CCCD", "Họ và tên", "Địa chỉ"])
        
        self.txt_timkiem = QLineEdit()
        self.txt_timkiem.setPlaceholderText("Nhập từ khóa tìm kiếm...")
        self.btn_timkiem = QPushButton("Tìm kiếm")

        layout_search.addWidget(QLabel("Tìm theo:"))
        layout_search.addWidget(self.cb_timkiem_theo)
        layout_search.addWidget(self.txt_timkiem)
        layout_search.addWidget(self.btn_timkiem)
        group_search.setLayout(layout_search)
        main_layout.addWidget(group_search)

        # --- Bảng hiển thị (Table) ---
        self.table_nhansu = QTableWidget()
        self.table_nhansu.setColumnCount(5)
        self.table_nhansu.setHorizontalHeaderLabels(["Số CCCD", "Họ và tên", "Ngày sinh", "Giới tính", "Địa chỉ"])
        self.table_nhansu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_nhansu.setSelectionBehavior(QTableWidget.SelectRows)
        main_layout.addWidget(self.table_nhansu)

        self.setLayout(main_layout)

        # --- KẾT NỐI SỰ KIỆN (SIGNALS) ---
        self.btn_them.clicked.connect(self.them_nhansu)
        self.btn_hienthi.clicked.connect(self.load_data)
        self.btn_xoa.clicked.connect(self.xoa_nhansu)
        self.btn_sua.clicked.connect(self.sua_nhansu)
        self.btn_timkiem.clicked.connect(self.timkiem_nhansu)
        
        # Click vào 1 dòng trong bảng sẽ điền dữ liệu lên Form
        self.table_nhansu.cellClicked.connect(self.dien_du_lieu_len_form)

    # ================= 3. CÁC HÀM XỬ LÝ DATABASE (CRUD) =================
    
    def load_data(self):
        """Hiển thị tất cả dữ liệu từ Database lên QTableWidget"""
        self.table_nhansu.setRowCount(0) # Xóa dữ liệu cũ trên bảng
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM NhanSu")
        rows = cursor.fetchall()
        
        for row_index, row_data in enumerate(rows):
            self.table_nhansu.insertRow(row_index)
            for col_index, data in enumerate(row_data):
                self.table_nhansu.setItem(row_index, col_index, QTableWidgetItem(str(data)))
        conn.close()

    def them_nhansu(self):
        """Thêm nhân sự mới vào CSDL"""
        cccd = self.txt_cccd.text()
        hoten = self.txt_hoten.text()
        ngaysinh = self.date_ngaysinh.text()
        gioitinh = self.cb_gioitinh.currentText()
        diachi = self.txt_diachi.text()

        if not cccd or not hoten:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ít nhất CCCD và Họ Tên!")
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # Dùng tham số (?) để tránh lỗi SQL Injection
            cursor.execute("INSERT INTO NhanSu VALUES (?, ?, ?, ?, ?)", (cccd, hoten, ngaysinh, gioitinh, diachi))
            conn.commit()
            QMessageBox.information(self, "Thành công", "Đã thêm nhân sự thành công!")
            self.load_data() # Tải lại bảng
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Lỗi", f"Số CCCD {cccd} đã tồn tại trong hệ thống!")
        finally:
            conn.close()

    def xoa_nhansu(self):
        """Xóa nhân sự dựa trên CCCD được chọn"""
        row = self.table_nhansu.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một nhân sự trên bảng để xóa!")
            return

        cccd = self.table_nhansu.item(row, 0).text()
        reply = QMessageBox.question(self, 'Xác nhận', f'Bạn có chắc chắn muốn xóa nhân sự có CCCD: {cccd}?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM NhanSu WHERE CCCD = ?", (cccd,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Thành công", "Đã xóa thành công!")
            self.load_data()

    def sua_nhansu(self):
        """Cập nhật thông tin nhân sự"""
        cccd = self.txt_cccd.text()
        hoten = self.txt_hoten.text()
        ngaysinh = self.date_ngaysinh.text()
        gioitinh = self.cb_gioitinh.currentText()
        diachi = self.txt_diachi.text()

        if not cccd:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập/chọn Số CCCD cần sửa!")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE NhanSu 
            SET HoTen = ?, NgaySinh = ?, GioiTinh = ?, DiaChi = ?
            WHERE CCCD = ?
        ''', (hoten, ngaysinh, gioitinh, diachi, cccd))
        
        if cursor.rowcount > 0:
            QMessageBox.information(self, "Thành công", "Đã cập nhật thông tin thành công!")
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy nhân sự với CCCD này!")
            
        conn.commit()
        conn.close()
        self.load_data()

    def timkiem_nhansu(self):
        """Tìm kiếm dữ liệu bằng câu lệnh LIKE"""
        tu_khoa = self.txt_timkiem.text()
        tieu_chi = self.cb_timkiem_theo.currentText()
        
        # Ánh xạ từ Combobox sang tên cột trong Database
        cot_tim_kiem = ""
        if tieu_chi == "Số CCCD": cot_tim_kiem = "CCCD"
        elif tieu_chi == "Họ và tên": cot_tim_kiem = "HoTen"
        elif tieu_chi == "Địa chỉ": cot_tim_kiem = "DiaChi"

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Thêm dấu % để tìm kiếm chứa từ khóa (LIKE %keyword%)
        cursor.execute(f"SELECT * FROM NhanSu WHERE {cot_tim_kiem} LIKE ?", ('%' + tu_khoa + '%',))
        rows = cursor.fetchall()
        conn.close()

        # Hiển thị kết quả tìm kiếm lên bảng
        self.table_nhansu.setRowCount(0)
        for row_index, row_data in enumerate(rows):
            self.table_nhansu.insertRow(row_index)
            for col_index, data in enumerate(row_data):
                self.table_nhansu.setItem(row_index, col_index, QTableWidgetItem(str(data)))

    def dien_du_lieu_len_form(self, row, col):
        """Hàm hỗ trợ: Khi click vào 1 dòng, tự động lấy dữ liệu điền ngược lên các ô nhập liệu"""
        self.txt_cccd.setText(self.table_nhansu.item(row, 0).text())
        self.txt_hoten.setText(self.table_nhansu.item(row, 1).text())
        
        # Xử lý chuỗi ngày tháng để đưa vào QDateEdit
        date_str = self.table_nhansu.item(row, 2).text()
        self.date_ngaysinh.setDate(QDate.fromString(date_str, "dd/MM/yyyy"))
        
        self.cb_gioitinh.setCurrentText(self.table_nhansu.item(row, 3).text())
        self.txt_diachi.setText(self.table_nhansu.item(row, 4).text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuanLyNhanSuApp()
    window.show()
    sys.exit(app.exec_())