from models.sanpham_model import SanPhamModel
from config.database import get_connection

class NvBanHangController:
    def __init__(self):
        self.model = SanPhamModel()

    def get_sanpham(self):
        return self.model.get_all()

    def get_customer_by_phone(self, phone):
        """Tìm khách hàng theo số điện thoại và trả về thông tin bao gồm điểm"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True) # Dùng dictionary để dễ truy cập theo tên cột
        try:
            sql = "SELECT id, ho_ten, dia_chi, diem_tich_luy FROM khach_hang WHERE so_dien_thoai = %s"
            cursor.execute(sql, (phone,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Lỗi tìm khách hàng: {e}")
            return None
        finally:
            conn.close()

    def save_invoice(self, cart_data, total, customer_id, id_nv, points_used, points_earned, 
                     loai_don_hang=0, dia_chi_giao="", trang_thai_giao=2, ghi_chu="", 
                     phuong_thuc="Tiền mặt", sdt_moi=None, ten_moi=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()

            # 1. Xử lý khách hàng (Giữ nguyên logic của bạn)
            final_customer_id = customer_id
            if not final_customer_id and sdt_moi and ten_moi:
                sql_ins_kh = "INSERT INTO khach_hang (ho_ten, so_dien_thoai, dia_chi, diem_tich_luy) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql_ins_kh, (ten_moi, sdt_moi, dia_chi_giao, points_earned))
                final_customer_id = cursor.lastrowid
                points_earned = 0 
                points_used = 0

            # 2. Lưu hóa đơn[cite: 15]
            sql_hd = """
                INSERT INTO hoa_don (
                    id_nhan_vien, id_khach_hang, tong_tien, ngay_lap, 
                    loai_don_hang, dia_chi_giao, trang_thai_giao, ghi_chu, phuong_thuc_thanh_toan
                ) VALUES (%s, %s, %s, NOW(), %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_hd, (id_nv, final_customer_id, total, loai_don_hang, 
                                    dia_chi_giao, trang_thai_giao, ghi_chu, phuong_thuc))
            id_hoa_don = cursor.lastrowid

            # 3. Lưu chi tiết & Trừ kho[cite: 15]
            for p_id, item in cart_data.items():
                qty = item['qty']
                price = float(item['info']['gia_ban'])
                
                cursor.execute("INSERT INTO chi_tiet_hoa_don (id_hoa_don, id_san_pham, so_luong, don_gia) VALUES (%s, %s, %s, %s)", 
                               (id_hoa_don, p_id, qty, price))
                
                cursor.execute("UPDATE san_pham SET so_luong_ton = so_luong_ton - %s WHERE id = %s", 
                               (qty, p_id))

            # 4. Cập nhật điểm khách hàng[cite: 15]
            if final_customer_id and (points_earned > 0 or points_used > 0):
                sql_diem = "UPDATE khach_hang SET diem_tich_luy = diem_tich_luy - %s + %s WHERE id = %s"
                cursor.execute(sql_diem, (points_used, points_earned, final_customer_id))

            # 5. QUAN TRỌNG: GHI LOG HOẠT ĐỘNG VÀO BẢNG MỚI TẠO
            hanh_dong = f"Đã thanh toán hóa đơn #{id_hoa_don} - Tổng: {total:,.0f}đ"
            sql_log = "INSERT INTO he_thong_log (id_nhan_vien, hanh_dong, thoi_gian) VALUES (%s, %s, NOW())"
            cursor.execute(sql_log, (id_nv, hanh_dong))

            conn.commit() 
            return True, "Thanh toán thành công!"
            
        except Exception as e:
            conn.rollback()
            print(f"Lỗi chi tiết: {str(e)}") # In lỗi ra Terminal để kiểm tra
            return False, f"Lỗi hệ thống: {str(e)}"
        finally:
            conn.close()