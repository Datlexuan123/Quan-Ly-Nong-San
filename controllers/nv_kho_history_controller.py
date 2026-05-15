# controllers/nv_kho_history_controller.py
from models.nhaphang_model import NhapHangModel

class NvKhoHistoryController:
    def __init__(self, view):
        self.view = view
        self.model = NhapHangModel()

    def load_history(self):
        """Hàm này phải tên là load_history để khớp với nv_main_view.py"""
        try:
            data = self.model.get_import_history()
            # Gọi hàm hiển thị bên View
            self.view.display_data(data)
        except Exception as e:
            print(f"Lỗi khi load lịch sử: {e}")