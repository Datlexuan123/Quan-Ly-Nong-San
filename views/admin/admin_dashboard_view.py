from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCharts import QChart, QChartView, QLineSeries
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from config.database import get_connection

class AdminDashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_real_data()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # 1. Khung chứa các thẻ thông báo nhanh (KPI Cards)
        card_layout = QHBoxLayout()
        # Khởi tạo card và lưu lại biến label để cập nhật dữ liệu
        self.card_doanh_thu, self.lbl_value_doanh_thu = self.create_card("DOANH THU HÔM NAY", "0 VNĐ", "#2e7d32")
        self.card_don_hang, self.lbl_value_don_hang = self.create_card("ĐƠN HÀNG MỚI", "0", "#1565c0")
        self.card_canh_bao, self.lbl_value_canh_bao = self.create_card("SẮP HẾT HÀNG", "0 Sản phẩm", "#d32f2f")
        
        card_layout.addWidget(self.card_doanh_thu)
        card_layout.addWidget(self.card_don_hang)
        card_layout.addWidget(self.card_canh_bao)
        self.layout.addLayout(card_layout)

        # 2. Khung chứa biểu đồ
        self.chart_view = self.create_revenue_chart()
        self.layout.addWidget(self.chart_view)

    def create_card(self, title, value, color):
        card = QFrame()
        card.setStyleSheet(f"background-color: {color}; border-radius: 10px; color: white;")
        card.setFixedHeight(100)
        l = QVBoxLayout(card)
        
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("font-size: 13px; font-weight: bold; border: none;")
        v_lbl = QLabel(value)
        v_lbl.setStyleSheet("font-size: 22px; font-weight: bold; border: none;")
        
        l.addWidget(t_lbl)
        l.addWidget(v_lbl)
        return card, v_lbl

    def create_revenue_chart(self):
        series = QLineSeries()
        # Giả lập dữ liệu cho biểu đồ
        series.append(0, 10); series.append(1, 20); series.append(2, 15); series.append(3, 30)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("XU HƯỚNG DOANH THU")
        chart.createDefaultAxes()
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        return chart_view

    def load_real_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # 1. Tính doanh thu hôm nay
            cursor.execute("SELECT SUM(tong_tien) as total FROM hoa_don WHERE DATE(ngay_lap) = CURDATE()")
            res_revenue = cursor.fetchone()
            today_revenue = res_revenue['total'] if res_revenue and res_revenue['total'] else 0
            self.lbl_value_doanh_thu.setText(f"{today_revenue:,.0f} VNĐ")

            # 2. Đếm sản phẩm sắp hết hàng (Dưới 10 đơn vị tồn)
            cursor.execute("SELECT COUNT(*) as total FROM san_pham WHERE so_luong_ton < 10")
            res_stock = cursor.fetchone()
            count_stock = res_stock['total'] if res_stock else 0
            self.lbl_value_canh_bao.setText(f"{count_stock} Sản phẩm")

            conn.close()
        except Exception as e:
            print(f"Lỗi nạp dữ liệu Dashboard: {e}")