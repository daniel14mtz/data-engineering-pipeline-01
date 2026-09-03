import psycopg2

from src.database import create_table, insert_data, count_users


def test_database_connection():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="dataeng",
        user="dataeng",
        password="dataeng"
    )

    assert conn is not None

    conn.close()

def test_insert_data_idempotent():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="dataeng",
        user="dataeng",
        password="dataeng"
    )

    create_table(conn)

    data = [
        {
            "id": 999,
            "name": "Juan",
            "email": "juan@example.com"
        }
    ]

    insert_data(conn, data)
    first_count = count_users(conn)

    insert_data(conn, data)
    second_count = count_users(conn)

    assert second_count == first_count

    conn.close()