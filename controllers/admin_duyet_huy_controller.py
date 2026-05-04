from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTableWidgetItem, QMessageBox

class AdminDuyetHuyController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.load_data() # Tự động tải dữ liệu khi mở trang

    def load_data(self):
        """Lấy danh sách các yêu cầu báo hủy đang chờ duyệt (trang_thai = 0)"""
        requests = self.model.get_pending_requests()
        self.view.table.setRowCount(0)
        
        for row, data in enumerate(requests):
            self.view.table.insertRow(row)
            # Hiển thị thông tin lên các cột
            self.view.table.setItem(row, 0, QTableWidgetItem(data['ho_ten'])) # NV báo
            self.view.table.setItem(row, 1, QTableWidgetItem(data['ten_sp'])) # Sản phẩm
            self.view.table.setItem(row, 2, QTableWidgetItem(str(data['so_luong_huy'])))
            self.view.table.setItem(row, 3, QTableWidgetItem(data['ly_do']))
            self.view.table.setItem(row, 4, QTableWidgetItem(str(data['ngay_huy'])))
            
            # Thêm nút bấm vào cột 5
            self.add_action_buttons(row, data)

    def add_action_buttons(self, row, data):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(2, 2, 2, 2)

        btn_yes = QPushButton("Đồng ý")
        btn_yes.setStyleSheet("background-color: #4caf50; color: white; font-weight: bold;")
        btn_yes.clicked.connect(lambda: self.process(data, 1)) # 1: Đồng ý duyệt

        btn_no = QPushButton("Từ chối")
        btn_no.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        btn_no.clicked.connect(lambda: self.process(data, 2)) # 2: Từ chối[cite: 4]

        layout.addWidget(btn_yes)
        layout.addWidget(btn_no)
        self.view.table.setCellWidget(row, 5, container)

    def process(self, data, xac_nhan):
        """Thực hiện phê duyệt hoặc từ chối[cite: 4]"""
        msg = "duyệt hủy" if xac_nhan == 1 else "từ chối yêu cầu hủy"
        reply = QMessageBox.question(self.view, "Xác nhận", f"Bạn có chắc muốn {msg} sản phẩm {data['ten_sp']}?")
        
        if reply == QMessageBox.StandardButton.Yes:
            # Gọi model để cập nhật DB và trừ kho nếu xac_nhan == 1[cite: 4]
            if self.model.duyet_huy_hang(data['id'], data['id_san_pham'], data['so_luong_huy'], xac_nhan):
                QMessageBox.information(self.view, "Thành công", "Đã cập nhật trạng thái thành công!")
                self.load_data() # Tải lại bảng sau khi duyệt xong
            else:
                QMessageBox.critical(self.view, "Lỗi", "Cập nhật thất bại!")