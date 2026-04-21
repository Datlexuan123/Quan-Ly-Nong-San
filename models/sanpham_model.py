from config.database import get_connection


class SanPhamModel:
    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM san_pham"
        cursor.execute(query)

        data = cursor.fetchall()
        conn.close()

        return data