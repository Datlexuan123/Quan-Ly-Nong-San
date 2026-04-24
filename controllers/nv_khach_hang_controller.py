from config.database import get_connection
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt

class NvKhachHangController: 
    def __init__(self, view):
        self.view = view
        self.view.btn_them.clicked.connect(self.them_khach)
        self.view.btn_lam_moi.clicked.connect(self.load_data)
        self.view.btn_search.clicked.connect(self.load_data)
        self.load_data()

    def load_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            txt = self.view.txt_search.text()
            
            # Câu lệnh SQL lấy đầy đủ các cột cần thiết
            sql = "SELECT id, ho_ten, so_dien_thoai, dia_chi, diem_tich_luy FROM khach_hang"
            if txt:
                sql += f" WHERE ho_ten LIKE '%{txt}%' OR so_dien_thoai LIKE '%{txt}%'"
            
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            self.view.table.setRowCount(0) # Xóa dữ liệu cũ trong bảng
            for row in rows:
                i = self.view.table.rowCount()
                self.view.table.insertRow(i)
                
                self.view.table.setItem(i, 0, QTableWidgetItem(str(row['id'])))
                self.view.table.setItem(i, 1, QTableWidgetItem(row['ho_ten']))
                self.view.table.setItem(i, 2, QTableWidgetItem(row['so_dien_thoai']))
                self.view.table.setItem(i, 3, QTableWidgetItem(row['dia_chi'] if row['dia_chi'] else ""))
                
                # HIỂN THỊ ĐIỂM TÍCH LŨY VÀO CỘT THỨ 5
                item_diem = QTableWidgetItem(str(row['diem_tich_luy']))
                item_diem.setTextAlignment(Qt.AlignmentFlag.AlignCenter) # Căn giữa số điểm
                self.view.table.setItem(i, 4, item_diem)
                
            conn.close()
        except Exception as e:
            print(f"Lỗi load dữ liệu khách hàng: {e}")

    def them_khach(self):
        ten = self.view.inp_ten.text().strip()
        sdt = self.view.inp_sdt.text().strip()
        dc = self.view.inp_dia_chi.text().strip()
        
        if not ten or not sdt:
            QMessageBox.warning(self.view, "Lỗi", "Vui lòng nhập Họ tên và SĐT")
            return
            
        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Thêm khách mới với điểm tích lũy mặc định là 0
            cursor.execute("INSERT INTO khach_hang (ho_ten, so_dien_thoai, dia_chi, diem_tich_luy) VALUES (%s, %s, %s, 0)", 
                           (ten, sdt, dc))
            conn.commit()
            conn.close()
            
            # Xóa trắng form và tải lại bảng
            self.view.inp_ten.clear()
            self.view.inp_sdt.clear()
            self.view.inp_dia_chi.clear()
            self.load_data()
            QMessageBox.information(self.view, "Thành công", f"Đã thêm khách hàng {ten}")
        except Exception as e:
            QMessageBox.critical(self.view, "Lỗi", f"Không thể thêm khách hàng: {e}")