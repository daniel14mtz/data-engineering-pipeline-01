import requests
import json
import psycopg2

URL = "https://jsonplaceholder.typicode.com/users"

def extract_data():
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    return response.json()

def validate_data(data):
    if not data:
        raise ValueError("No se recibieron datos")

    required_fields = {"id", "name", "email"}

    for record in data:
        missing_fields = required_fields - record.keys()

        if missing_fields:
            raise ValueError(
                f"Faltan campos en el registro {record.get('id')}: {missing_fields}"
            )

    ids = [record["id"] for record in data]

    if len(ids) != len(set(ids)):
        raise ValueError("Existen IDs duplicados")

    print(f"Validacion correcta: {len(data)} registros")

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

    print(f"{len(data)} registros insertados en PostgreSQL")


def save_json(data):
    with open("data/users.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Datos guardados en json")

def main():
    data = extract_data()
    validate_data(data)

    conn = connect_db()

    try:
        create_table(conn)
        insert_data(conn, data)
    finally:
        conn.close()

    save_json(data)

if __name__ == "__main__":
    main()