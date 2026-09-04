import os

API_URL = os.getenv(
    "API_URL",
    "https://jsonplaceholder.typicode.com/users"
)

RAW_PATH = os.getenv(
    "RAW_PATH",
    "data/raw/users.json"
)

PROCESSED_PATH = os.getenv(
    "PROCESSED_PATH",
    "data/processed/users.json"
)