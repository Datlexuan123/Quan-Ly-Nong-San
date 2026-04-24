from models.sanpham_model import SanPhamModel
from config.database import get_connection

class NvBanHangController:
    def __init__(self):
        self.model = SanPhamModel()

    def get_sanpham(self):
        return self.model.get_all()

    def save_invoice(self, cart_data, total, customer_id, id_nv, points_used, points_earned, 
                     loai_don_hang=0, dia_chi_giao="", trang_thai_giao=2, ghi_chu="", phuong_thuc="Tiền mặt"):
        """
        Lưu hóa đơn tích hợp phân loại đơn ship và phương thức thanh toán
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()

            # 1. Lưu hóa đơn vào bảng hoa_don
            sql_hd = """
                INSERT INTO hoa_don (
                    id_nhan_vien, id_khach_hang, tong_tien, ngay_lap, 
                    loai_don_hang, dia_chi_giao, trang_thai_giao, ghi_chu, phuong_thuc_thanh_toan
                ) VALUES (%s, %s, %s, NOW(), %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_hd, (id_nv, customer_id, total, loai_don_hang, 
                                    dia_chi_giao, trang_thai_giao, ghi_chu, phuong_thuc))
            id_hoa_don = cursor.lastrowid

            # 2. Lưu chi tiết & Trừ kho
            for p_id, item in cart_data.items():
                qty = item['qty']
                price = float(item['info']['gia_ban'])
                
                sql_ct = "INSERT INTO chi_tiet_hoa_don (id_hoa_don, id_san_pham, so_luong, don_gia) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql_ct, (id_hoa_don, p_id, qty, price))
                
                sql_update_kho = "UPDATE san_pham SET so_luong_ton = so_luong_ton - %s WHERE id = %s"
                cursor.execute(sql_update_kho, (qty, p_id))

            # 3. Cập nhật điểm khách hàng
            if customer_id:
                sql_diem = "UPDATE khach_hang SET diem_tich_luy = diem_tich_luy - %s + %s WHERE id = %s"
                cursor.execute(sql_diem, (points_used, points_earned, customer_id))

            conn.commit() 
            return True, "Thanh toán thành công!"
            
        except Exception as e:
            conn.rollback()
            return False, f"Lỗi hệ thống: {str(e)}"
        finally:
            conn.close()