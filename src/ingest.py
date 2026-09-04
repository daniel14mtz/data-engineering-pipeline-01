import requests
import json
import logging 
import time

from src.database import connect_db, create_table, insert_data, count_loaded_users
from src.transform import validate_data, transform_data

from src.config import API_URL, RAW_PATH, PROCESSED_PATH

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def extract_data():
    logger.info("Iniciando extraccion de datos")

    max_retries = 3

    for attempt in range(1, max_retries + 1):

        try:
            response = requests.get(API_URL, timeout=10)
            response.raise_for_status()

            data = response.json()

            logger.info(f"Extraccion completada: {len(data)} registros")

            return data

        except requests.RequestException as e:
            logger.error(
                f"Error en la extraccion. "
                f"Intento {attempt}/{max_retries}: {e}"
            )

            if attempt < max_retries:
                wait_time = 2 ** attempt

                logger.info(
                    f"Reintentando en {wait_time} segundos..."
                )

                time.sleep(wait_time)
            else:
                logger.error(
                    "Se agotaron los reintentos de extraccion"
                )
                raise

def save_json(data, path):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)

    logger.info(f"Datos guardados en {path}")

def load_data(data):
    logger.info("Conectando a PostgreSQL")

    conn = None

    try:
        conn = connect_db()

        create_table(conn)
        insert_data(conn, data)

        logger.info("Datos guardados en PostgreSQL")

        loaded_count = count_loaded_users(conn, data)

        if loaded_count != len(data):
            raise ValueError(
                f"Data Quality Error: esperados {len(data)}, encontrados {loaded_count}"
            )

        logger.info(f"Data Quality OK: {loaded_count} registros cargados")

    except Exception as e:
        logger.error(f"Error en la carga a PostgreSQL: {e}")
        raise

    finally:
        if conn is not None:
            conn.close()

def main():
    data = extract_data()

    save_json(data, RAW_PATH)

    validate_data(data)

    data = transform_data(data)

    load_data(data)

    save_json(data, PROCESSED_PATH)

if __name__ == "__main__":
    main()