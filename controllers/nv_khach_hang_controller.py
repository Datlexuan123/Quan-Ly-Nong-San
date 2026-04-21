from config.database import get_connection
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox

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
            sql = "SELECT * FROM khach_hang"
            if txt:
                sql += f" WHERE ho_ten LIKE '%{txt}%' OR so_dien_thoai LIKE '%{txt}%'"
            
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.view.table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                self.view.table.setItem(i, 0, QTableWidgetItem(str(row['id'])))
                self.view.table.setItem(i, 1, QTableWidgetItem(row['ho_ten']))
                self.view.table.setItem(i, 2, QTableWidgetItem(row['so_dien_thoai']))
                self.view.table.setItem(i, 3, QTableWidgetItem(row['dia_chi']))
            conn.close()
        except Exception as e:
            print(f"Lỗi DB: {e}")

    def them_khach(self):
        ten, sdt, dc = self.view.inp_ten.text(), self.view.inp_sdt.text(), self.view.inp_dia_chi.text()
        if not ten or not sdt:
            QMessageBox.warning(self.view, "Lỗi", "Nhập đủ Tên và SĐT")
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO khach_hang (ho_ten, so_dien_thoai, dia_chi) VALUES (%s, %s, %s)", (ten, sdt, dc))
            conn.commit()
            conn.close()
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self.view, "Lỗi", str(e))