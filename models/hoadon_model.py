import mysql.connector
from datetime import datetime

class HoaDonModel:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'cuahang_nongsan'
        }

    def get_orders_by_type(self, is_ship=True, status=None):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            loai_don = 1 if is_ship else 0
            query = """
                SELECT hd.*, kh.ho_ten as ten_khach, nv.ho_ten as ten_nv 
                FROM hoa_don hd
                LEFT JOIN khach_hang kh ON hd.id_khach_hang = kh.id
                LEFT JOIN nhan_vien nv ON hd.id_nhan_vien = nv.id
                WHERE hd.loai_don_hang = %s
            """
            params = [loai_don]
            if status is not None and status != -1:
                query += " AND hd.trang_thai_giao = %s"
                params.append(status)
            query += " ORDER BY hd.ngay_lap DESC"
            
            cursor.execute(query, tuple(params))
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi lấy đơn hàng: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def update_status(self, order_id, new_status):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            query = "UPDATE hoa_don SET trang_thai_giao = %s WHERE id = %s"
            cursor.execute(query, (new_status, order_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi cập nhật trạng thái: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def update_order_info(self, order_id, new_address, editor_name):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            time_now = datetime.now().strftime("%H:%M %d/%m/%Y")
            log_entry = f"\n[Sửa địa chỉ bởi: {editor_name} lúc {time_now}]"
            query = """
                UPDATE hoa_don 
                SET dia_chi_giao = %s, 
                    ghi_chu = CONCAT(IFNULL(ghi_chu, ''), %s) 
                WHERE id = %s
            """
            cursor.execute(query, (new_address, log_entry, order_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi update: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()