import logging

logger = logging.getLogger(__name__)

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

        if not isinstance(record["id"], int):
            raise ValueError(
                f"El ID del registro debe ser entero: {record['id']}"
            )

        if not record["name"].strip():
            raise ValueError(
                f"El nombre del registro {record['id']} no puede estar vacío"
            )

        if "@" not in record["email"] or "." not in record["email"].split("@")[-1]:
            raise ValueError(
                f"Email inválido en el registro {record['id']}: {record['email']}"
            )

    ids = [record["id"] for record in data]

    if len(ids) != len(set(ids)):
        raise ValueError("Existen IDs duplicados")

    logger.info(f"Validacion correcta: {len(data)} registros")

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