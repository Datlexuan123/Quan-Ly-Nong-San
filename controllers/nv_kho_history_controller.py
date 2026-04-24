from models.nhaphang_model import NhapHangModel

class NvKhoHistoryController:
    def __init__(self, view):
        self.view = view
        self.model = NhapHangModel()
        self.load_history()

    def load_history(self):
        data = self.model.get_import_history()
        self.view.display_data(data)