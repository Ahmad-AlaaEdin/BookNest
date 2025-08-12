from ..database import get_db_connection


class Book :
    def create(self,user_id,title,status):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO book(user_id,title,status) VALUES() ")
        conn.close()
    def update(self,user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute()
        conn.close()
    def delete(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute()
        conn.close()
