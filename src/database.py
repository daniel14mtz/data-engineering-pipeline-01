import psycopg2

def connect_db():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="dataeng",
        user="dataeng",
        password="dataeng"
    )

def create_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(150)
        );
    """)

    conn.commit()
    cursor.close()

    print("Table users lista")

def insert_data(conn, data):
    cursor = conn.cursor()

    query = """
        INSERT INTO users (id, name, email)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO UPDATE
        SET name = EXCLUDED.name,
            email = EXCLUDED.email;
    """

    for user in data:
        cursor.execute(
            query,
            (
                user["id"],
                user["name"],
                user["email"]
            )
        )

    conn.commit()
    cursor.close()

def count_users(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users;")

    count = cursor.fetchone()[0]

    cursor.close()

    return count