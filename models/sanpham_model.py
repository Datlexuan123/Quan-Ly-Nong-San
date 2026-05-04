from config.database import get_connection

class SanPhamModel:
    def get_all(self):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            # Đảm bảo lấy đủ cột trang_thai
            cursor.execute("SELECT * FROM san_pham")
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi lấy sản phẩm: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_status(self, product_id, new_status):
        """Cập nhật trạng thái kinh doanh của sản phẩm vào DB"""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "UPDATE san_pham SET trang_thai = %s WHERE id = %s"
            cursor.execute(sql, (new_status, product_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi cập nhật trạng thái: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()