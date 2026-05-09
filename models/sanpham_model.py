# models/sanpham_model.py
from config.database import get_connection

class SanPhamModel:
    def get_all(self, search_text=""):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            # SỬA: Thêm subquery tính AVG(gia_nhap) làm giá vốn TB
            sql = """
                SELECT s.*, d.ten_dvt,
                (SELECT AVG(gia_nhap) FROM chi_tiet_nhap_hang WHERE id_san_pham = s.id) as gia_von_tb
                FROM san_pham s
                LEFT JOIN don_vi_tinh d ON s.id_dvt = d.id
                WHERE s.ten_sp LIKE %s
                ORDER BY s.id ASC
            """
            cursor.execute(sql, (f"%{search_text}%",))
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi SQL get_all: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_import_history(self, product_id):
        """Lấy lịch sử nhập hàng kèm giá vốn trung bình"""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            # Truy vấn lấy từng lô và dùng Subquery để tính AVG(gia_nhap)
            sql = """
                SELECT 
                    n.ngay_nhap, c.so_luong_nhap, c.gia_nhap, ncc.ten_ncc,
                    (SELECT AVG(gia_nhap) FROM chi_tiet_nhap_hang WHERE id_san_pham = %s) as gia_von_tb
                FROM chi_tiet_nhap_hang c
                JOIN nhap_hang n ON c.id_nhap_hang = n.id
                JOIN nha_cung_cap ncc ON n.id_nha_cung_cap = ncc.id
                WHERE c.id_san_pham = %s
                ORDER BY n.ngay_nhap DESC
            """
            cursor.execute(sql, (product_id, product_id))
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi SQL lấy lịch sử: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def add_product(self, data):
        """Thêm sản phẩm mới từ dữ liệu Dialog"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = """INSERT INTO san_pham (ten_sp, gia_ban, hinh_anh, han_su_dung, id_dvt, so_luong_ton) 
                     VALUES (%s, %s, %s, %s, %s, 0)"""
            cursor.execute(sql, (data['ten'], data['gia'], data['anh'], data['hsd'], data['dvt']))
            conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi thêm SP: {e}")
            return False
        finally:
            conn.close()

    def update_product(self, p_id, data):
        """Cập nhật sản phẩm"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "UPDATE san_pham SET gia_ban = %s, hinh_anh = %s, id_dvt = %s WHERE id = %s"
            cursor.execute(sql, (data['gia'], data['anh'], data['dvt'], p_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi sửa SP: {e}")
            return False
        finally:
            conn.close()

    def delete_product(self, p_id):
        """Xóa sản phẩm nếu tồn kho = 0"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT so_luong_ton FROM san_pham WHERE id = %s", (p_id,))
            res = cursor.fetchone()
            if res and res[0] > 0:
                return False # Không được xóa nếu còn hàng
            
            cursor.execute("DELETE FROM san_pham WHERE id = %s", (p_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi xóa SP: {e}")
            return False
        finally:
            conn.close()

    def update_status(self, product_id, new_status):
        """Ẩn/Hiện sản phẩm"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE san_pham SET trang_thai = %s WHERE id = %s", (new_status, product_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi trạng thái: {e}")
            return False
        finally:
            conn.close()