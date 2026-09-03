import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="dataeng",
    user="dataeng",
    password="dataeng"
)

print("Conexion exitosa a PostgreSQL")

conn.close()