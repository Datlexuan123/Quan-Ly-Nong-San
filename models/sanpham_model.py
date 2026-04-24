from config.database import get_connection
class SanPhamModel:
    def get_all(self):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM san_pham")
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi lấy sản phẩm: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()