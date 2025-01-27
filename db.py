import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname="support_db",
            user="admin",
            password="root",
            host="127.0.0.1",
            port=5432,
        )
        return connection
    except Exception as e:
        print("Ошибка подключения к базе данных:", e)
        raise

def fetch_query(query, params=None):
    connection = get_db_connection()
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()  
            return result
    except Exception as e:
        print("Ошибка выполнения запроса:", e)
        raise
    finally:
        connection.close()
