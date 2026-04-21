from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QHeaderView, QTabWidget, QDateEdit, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QDate
from config.database import get_connection

# Thêm thư viện vẽ sơ đồ
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class AdminBaoCaoView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        # Nạp dữ liệu mặc định ngay khi mở trang
        self.load_revenue_data() 
        self.load_inventory_data()
        self.load_customer_data()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # 1. TIÊU ĐỀ & BỘ LỌC TỔNG
        header_row = QHBoxLayout()
        title = QLabel("HỆ THỐNG BÁO CÁO & THỐNG KÊ")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1b5e20;")
        header_row.addWidget(title)
        
        header_row.addStretch()
        header_row.addWidget(QLabel("Từ:"))
        self.date_from = QDateEdit(QDate(2026, 4, 1))
        self.date_from.setCalendarPopup(True)
        header_row.addWidget(self.date_from)
        
        header_row.addWidget(QLabel("Đến:"))
        self.date_to = QDateEdit(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        header_row.addWidget(self.date_to)
        
        self.btn_refresh = QPushButton("🔄 Cập nhật")
        self.btn_refresh.setStyleSheet("background-color: #2e7d32; color: white; padding: 5px 15px; font-weight: bold;")
        self.btn_refresh.clicked.connect(self.refresh_all_reports)
        header_row.addWidget(self.btn_refresh)
        self.layout.addLayout(header_row)

        # 2. KHU VỰC TỔNG QUAN
        self.summary_layout = QHBoxLayout()
        self.card_doanhthu = self.create_summary_card("TỔNG DOANH THU", "0 đ", "#e8f5e9", "#2e7d32")
        self.card_loinhuan = self.create_summary_card("TỔNG LỢI NHUẬN", "0 đ", "#e3f2fd", "#1565c0")
        self.card_donhang = self.create_summary_card("TỔNG ĐƠN HÀNG", "0", "#fff3e0", "#ef6c00")
        
        self.summary_layout.addWidget(self.card_doanhthu)
        self.summary_layout.addWidget(self.card_loinhuan)
        self.summary_layout.addWidget(self.card_donhang)
        self.layout.addLayout(self.summary_layout)

        # 3. KHU VỰC SƠ ĐỒ
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.layout.addWidget(self.canvas)

        # 4. HỆ THỐNG TAB
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_revenue_table_tab(), "📋 Chi tiết doanh thu")
        self.tabs.addTab(self.create_inventory_tab(), "📦 Kho & Hàng hủy")
        self.tabs.addTab(self.create_customer_tab(), "👥 Khách hàng")
        self.layout.addWidget(self.tabs)

    def create_summary_card(self, title, value, bg_color, text_color):
        card = QFrame()
        card.setStyleSheet(f"background-color: {bg_color}; border-radius: 10px; border: 1px solid #ddd;")
        l = QVBoxLayout(card)
        t = QLabel(title); t.setStyleSheet(f"color: {text_color}; font-weight: bold; border: none;")
        v = QLabel(value); v.setStyleSheet(f"color: {text_color}; font-size: 20px; font-weight: bold; border: none;")
        l.addWidget(t); l.addWidget(v)
        card.value_label = v
        return card

    def create_revenue_table_tab(self):
        self.table_revenue = QTableWidget()
        self.table_revenue.setColumnCount(4)
        self.table_revenue.setHorizontalHeaderLabels(["Ngày Lập", "Số Đơn", "Doanh Thu", "Lợi Nhuận"])
        self.table_revenue.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        return self.table_revenue

    def refresh_all_reports(self):
        self.load_revenue_data()
        self.load_inventory_data()
        self.load_customer_data()

    def load_revenue_data(self):
        d1 = self.date_from.date().toString("yyyy-MM-dd")
        d2 = self.date_to.date().toString("yyyy-MM-dd")
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    DATE(h.ngay_lap) as ngay, 
                    COUNT(DISTINCT h.id) as so_don,
                    SUM(h.tong_tien) as doanh_thu,
                    SUM(ct.so_luong * (ct.don_gia - IFNULL((SELECT AVG(gia_nhap) FROM chi_tiet_nhap_hang WHERE id_san_pham = ct.id_san_pham), 0))) as loi_nhuan
                FROM hoa_don h
                JOIN chi_tiet_hoa_don ct ON h.id = ct.id_hoa_don
                WHERE DATE(h.ngay_lap) BETWEEN %s AND %s
                GROUP BY DATE(h.ngay_lap) ORDER BY ngay ASC
            """
            cursor.execute(query, (d1, d2))
            rows = cursor.fetchall()
            
            total_dt = 0; total_ln = 0; total_don = 0
            dates = []; revenues = []

            self.table_revenue.setRowCount(0)
            for r in rows:
                total_dt += float(r['doanh_thu'])
                total_ln += float(r['loi_nhuan'])
                total_don += int(r['so_don'])
                dates.append(str(r['ngay']))
                revenues.append(float(r['doanh_thu']))

                row = self.table_revenue.rowCount()
                self.table_revenue.insertRow(row)
                self.table_revenue.setItem(row, 0, QTableWidgetItem(str(r['ngay'])))
                self.table_revenue.setItem(row, 1, QTableWidgetItem(str(r['so_don'])))
                self.table_revenue.setItem(row, 2, QTableWidgetItem(f"{float(r['doanh_thu']):,.0f} đ"))
                self.table_revenue.setItem(row, 3, QTableWidgetItem(f"{float(r['loi_nhuan']):,.0f} đ"))

            self.card_doanhthu.value_label.setText(f"{total_dt:,.0f} đ")
            self.card_loinhuan.value_label.setText(f"{total_ln:,.0f} đ")
            self.card_donhang.value_label.setText(str(total_don))

            self.update_chart(dates, revenues)
            conn.close()
        except Exception as e:
            print(f"Lỗi tải doanh thu: {e}")

    def update_chart(self, dates, revenues):
        self.canvas.figure.clf()
        ax = self.canvas.figure.add_subplot(111)
        if dates:
            ax.bar(dates, revenues, color='#2e7d32')
            ax.set_title("Biểu đồ doanh thu theo ngày")
            ax.set_ylabel("VNĐ")
            # Xoay chữ ngày để dễ nhìn nếu nhiều dữ liệu
            self.canvas.figure.autofmt_xdate()
        self.canvas.draw()

    # --- CÁC HÀM QUAN TRỌNG PHẢI NẰM TRONG CLASS ---
    def create_inventory_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)
        self.table_inventory = QTableWidget()
        self.table_inventory.setColumnCount(4)
        self.table_inventory.setHorizontalHeaderLabels(["ID", "Sản Phẩm", "Tồn", "Nguồn"])
        self.table_inventory.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        l.addWidget(self.table_inventory)
        return w

    def load_inventory_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            self.table_inventory.setRowCount(0)
            cursor.execute("SELECT id, ten_sp, so_luong_ton, nguon_goc FROM san_pham")
            for r in cursor.fetchall():
                row = self.table_inventory.rowCount()
                self.table_inventory.insertRow(row)
                self.table_inventory.setItem(row, 0, QTableWidgetItem(str(r['id'])))
                self.table_inventory.setItem(row, 1, QTableWidgetItem(r['ten_sp']))
                self.table_inventory.setItem(row, 2, QTableWidgetItem(str(r['so_luong_ton'])))
                self.table_inventory.setItem(row, 3, QTableWidgetItem(str(r['nguon_goc'])))
            conn.close()
        except Exception as e:
            print(f"Lỗi tải kho: {e}")

    def create_customer_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)
        self.table_customer = QTableWidget()
        self.table_customer.setColumnCount(4)
        self.table_customer.setHorizontalHeaderLabels(["Tên", "SĐT", "Đơn", "Chi tiêu"])
        self.table_customer.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        l.addWidget(self.table_customer)
        return w

    def load_customer_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            self.table_customer.setRowCount(0)
            query = """
                SELECT k.ho_ten, k.so_dien_thoai, COUNT(h.id) as tong_don, SUM(h.tong_tien) as tong_chi 
                FROM khach_hang k 
                LEFT JOIN hoa_don h ON k.id = h.id_khach_hang 
                GROUP BY k.id 
                ORDER BY tong_chi DESC
            """
            cursor.execute(query)
            for r in cursor.fetchall():
                row = self.table_customer.rowCount()
                self.table_customer.insertRow(row)
                self.table_customer.setItem(row, 0, QTableWidgetItem(str(r['ho_ten'])))
                self.table_customer.setItem(row, 1, QTableWidgetItem(str(r['so_dien_thoai'])))
                self.table_customer.setItem(row, 2, QTableWidgetItem(str(r['tong_don'])))
                chi = r['tong_chi'] if r['tong_chi'] else 0
                self.table_customer.setItem(row, 3, QTableWidgetItem(f"{float(chi):,.0f} đ"))
            conn.close()
        except Exception as e:
            print(f"Lỗi tải khách hàng: {e}")