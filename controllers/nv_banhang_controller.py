from models.sanpham_model import SanPhamModel


class NvBanHangController:
    def __init__(self):
        self.model = SanPhamModel()

    def get_sanpham(self):
        return self.model.get_all()