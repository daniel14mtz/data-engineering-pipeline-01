import psycopg2


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
