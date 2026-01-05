import requests
from pathlib import Path

DOCS = {
    "time_travel": "https://docs.snowflake.com/en/user-guide/data-time-travel",
    "warehouses": "https://docs.snowflake.com/en/user-guide/warehouses",
}

RAW_PATH = Path("data/raw_docs")
RAW_PATH.mkdir(parents=True, exist_ok=True)

def download_docs():
    for name, url in DOCS.items():
        response = requests.get(url)
        response.raise_for_status()

        file_path = RAW_PATH / f"{name}.html"
        file_path.write_text(response.text, encoding="utf-8")
        print(f"Downloaded {name}")

if __name__ == "__main__":
    download_docs()
