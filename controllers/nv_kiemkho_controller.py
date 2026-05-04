# controllers/nv_kiemkho_controller.py

from models.kiemkho_model import KiemKhoModel
from PyQt6.QtWidgets import QMessageBox

class NvKiemKhoController: # Tên Class phải viết hoa chữ cái đầu như thế này
    def __init__(self, view, user_data):
        self.view = view
        self.user_data = user_data if user_data else {}
        self.model = KiemKhoModel()
        
        # Tải danh sách sản phẩm lên giao diện[cite: 4]
        self.load_products()
        
        # Kết nối nút bấm xác nhận báo hủy[cite: 4]
        self.view.btn_confirm.clicked.connect(self.handle_bao_huy)

    def load_products(self):
        """Lấy danh sách sản phẩm từ database[cite: 4]"""
        self.products = self.model.get_all_products()
        self.view.cbo_sp.clear()
        for p in self.products:
            # Hiển thị tên kèm số lượng tồn kho[cite: 4]
            self.view.cbo_sp.addItem(f"{p['ten_sp']} (Tồn: {p['so_luong_ton']})", p['id'])

    def handle_bao_huy(self):
        """Gửi yêu cầu báo hủy chờ Admin phê duyệt[cite: 4]"""
        sp_id = self.view.cbo_sp.currentData()
        sl = self.view.spin_qty.value()
        ly_do = self.view.txt_lydo.toPlainText().strip()
        
        # Lấy ID nhân viên đang đăng nhập[cite: 4]
        nv_id = self.user_data.get('id', 1)

        if sl <= 0:
            QMessageBox.warning(self.view, "Lỗi", "Số lượng báo hủy phải lớn hơn 0!")
            return

        if not ly_do:
            QMessageBox.warning(self.view, "Lỗi", "Vui lòng nhập lý do báo hủy!")
            return

        # Gọi model lưu yêu cầu vào database (trạng thái chờ duyệt)
        if self.model.bao_huy_hang(sp_id, nv_id, sl, ly_do):
            QMessageBox.information(self.view, "Thành công", 
                                    "Đã gửi yêu cầu báo hủy. Vui lòng chờ Admin phê duyệt!")
            self.view.txt_lydo.clear()
            self.view.spin_qty.setValue(0.1)
            self.load_products()
        else:
            QMessageBox.critical(self.view, "Lỗi", "Không thể gửi yêu cầu báo hủy!")