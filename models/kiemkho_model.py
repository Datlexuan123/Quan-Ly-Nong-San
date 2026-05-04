# models/kiemkho_model.py
from config.database import get_connection

class KiemKhoModel:
    def get_all_products(self):
        """Lấy danh sách sản phẩm để chọn báo hủy"""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            # Chỉ lấy sản phẩm đang kinh doanh (trang_thai = 0)
            cursor.execute("SELECT id, ten_sp, so_luong_ton FROM san_pham WHERE trang_thai = 0")
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi lấy SP: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def bao_huy_hang(self, id_sp, id_nv, so_luong, ly_do):
        """Nhân viên gửi yêu cầu báo hủy (Trạng thái mặc định = 0: Chờ duyệt)[cite: 4]"""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Thêm vào bảng hủy với trạng thái = 0, chưa trừ kho[cite: 4]
            sql = "INSERT INTO thanh_ly_huy_hang (id_san_pham, id_nhan_vien, so_luong_huy, ngay_huy, ly_do, trang_thai) VALUES (%s, %s, %s, NOW(), %s, 0)"
            cursor.execute(sql, (id_sp, id_nv, so_luong, ly_do))
            conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi gửi yêu cầu hủy: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_pending_requests(self):
        """Admin lấy các yêu cầu đang chờ duyệt (trang_thai = 0)"""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            sql = """
                SELECT t.*, s.ten_sp, n.ho_ten 
                FROM thanh_ly_huy_hang t
                JOIN san_pham s ON t.id_san_pham = s.id
                JOIN nhan_vien n ON t.id_nhan_vien = n.id
                WHERE t.trang_thai = 0
            """
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi lấy yêu cầu chờ duyệt: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def duyet_huy_hang(self, id_huy, id_sp, so_luong, xac_nhan):
        """Admin phê duyệt: xac_nhan=1 (Đồng ý), xac_nhan=2 (Từ chối)[cite: 4]"""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            # 1. Cập nhật trạng thái yêu cầu[cite: 4]
            cursor.execute("UPDATE thanh_ly_huy_hang SET trang_thai = %s WHERE id = %s", (xac_nhan, id_huy))
            
            # 2. Nếu đồng ý thì mới trừ kho[cite: 4]
            if xac_nhan == 1:
                cursor.execute("UPDATE san_pham SET so_luong_ton = so_luong_ton - %s WHERE id = %s", (so_luong, id_sp))
                
                # Ghi log hoạt động phê duyệt
                sql_log = "INSERT INTO he_thong_log (id_nhan_vien, hanh_dong, thoi_gian) VALUES (%s, %s, NOW())"
                hanh_dong = f"Admin duyệt hủy SP ID:{id_sp} - SL:{so_luong}"
                cursor.execute(sql_log, (1, hanh_dong)) # Mặc định ID Admin là 1
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi phê duyệt: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()