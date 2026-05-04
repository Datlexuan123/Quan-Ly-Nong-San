from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from config.database import get_connection

class AdminLogView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel("🛡️ NHẬT KÝ HOẠT ĐỘNG HỆ THỐNG")
        header.setStyleSheet("font-size:20px; font-weight:bold; color:#d32f2f; margin-bottom: 10px;")
        layout.addWidget(header)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Thời gian", "Nhân viên", "Hành động"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        self.load_data() # Gọi hàm load khi mở trang

    def load_data(self):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            # Truy vấn lấy dữ liệu từ bảng he_thong_log và nhan_vien
            query = """
                SELECT l.thoi_gian, nv.ho_ten, l.hanh_dong 
                FROM he_thong_log l
                JOIN nhan_vien nv ON l.id_nhan_vien = nv.id
                ORDER BY l.thoi_gian DESC
            """
            cursor.execute(query)
            logs = cursor.fetchall()
            
            self.table.setRowCount(len(logs))
            for row, log in enumerate(logs):
                # Cột 0: Thời gian
                self.table.setItem(row, 0, QTableWidgetItem(str(log['thoi_gian'])))
                
                # Cột 1: Nhân viên
                self.table.setItem(row, 1, QTableWidgetItem(log['ho_ten']))
                
                # Cột 2: Hành động (ĐÂY LÀ DÒNG BẠN CẦN KIỂM TRA KỸ)[cite: 8]
                hanh_dong_text = log.get('hanh_dong', '') # Lấy giá trị từ key 'hanh_dong'[cite: 8]
                self.table.setItem(row, 2, QTableWidgetItem(str(hanh_dong_text)))
                
        except Exception as e:
            print(f"Lỗi hiển thị nhật ký: {e}")
        finally:
            if conn:
                conn.close()