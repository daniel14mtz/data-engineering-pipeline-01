import requests
import json
import logging 

from src.database import connect_db, create_table, insert_data, count_users

URL = "https://jsonplaceholder.typicode.com/users"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def extract_data():
    logger.info("Iniciando extraccion de datos")

    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()

        data = response.json()

        logger.info(f"Extraccion completada: {len(data)} registros")

        return data

    except requests.RequestException as e:
        logger.error(f"Error en la extraccion: {e}")
        raise

def transform_data(data):
    transformed_data = []

    for user in data:
        transformed_data.append({
            "id": user["id"],
            "name": user["name"].strip(),
            "email": user["email"].strip().lower()
        })

    logger.info(f"Transformacion correcta: {len(transformed_data)} registros")

    return transformed_data

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

    logger.info(f"Validacion correcta: {len(data)} registros")


def save_json(data, path):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)

    logger.info(f"Datos guardados en {path}")

def main():
    data = extract_data()

    save_json(data, "data/raw/users.json")

    validate_data(data)

    data = transform_data(data)

    save_json(data, "data/processed/users.json")

    try:

        logger.info("Conectando a PostgreSQL")

        conn = connect_db()

        create_table(conn)
        insert_data(conn, data)

        logger.info("Datos guardados en PostgreSQL")

        loaded_count = count_users(conn)

        if loaded_count != len(data):
            raise ValueError(
                f"Data Quality Error: esperados {len(data)}, encontrados {loaded_count}"
            )

        logger.info(f"Data Quality OK: {loaded_count} registros cargados")

    except Exception as e:
        logger.error(f"Error en la carga a PostgreSQL: {e}")
        raise
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()