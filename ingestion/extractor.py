import requests
from pathlib import Path

#RAG is going to be based on business continuity and data recovery on Snowflake
DOCS = {
    "time_travel": "https://docs.snowflake.com/en/user-guide/data-time-travel",
    "replication_introduction": "https://docs.snowflake.com/en/user-guide/account-replication-intro",
    "replication_considerations": "https://docs.snowflake.com/en/user-guide/account-replication-considerations",
    "replication_config": "https://docs.snowflake.com/en/user-guide/account-replication-config",
    "security_integrations": "https://docs.snowflake.com/en/user-guide/account-replication-security-integrations",
    "iceberg_replication": "https://docs.snowflake.com/en/user-guide/tables-iceberg-replication",
    "stage_pipes_load_history": "https://docs.snowflake.com/en/user-guide/account-replication-stages-pipes-load-history",
    "git_repository_replication": "https://docs.snowflake.com/en/user-guide/account-replication-git-repositories",
    "replication_cost": "https://docs.snowflake.com/en/user-guide/account-replication-cost",
    "replication_failover": "https://docs.snowflake.com/en/user-guide/account-replication-failover-failback",
    "replication_monitor": "https://docs.snowflake.com/en/user-guide/account-replication-monitor",
    "replication_error_notifications": "https://docs.snowflake.com/en/user-guide/account-replication-error-notifications",
    "replication_client_redirect": "https://docs.snowflake.com/en/user-guide/client-redirect",
    "replication_backups": "https://docs.snowflake.com/en/user-guide/backups",
    "replication_time_travel": "https://docs.snowflake.com/en/user-guide/data-time-travel",
    "replication_failsafe": "https://docs.snowflake.com/en/user-guide/data-failsafe",
    "replication_storage_costs": "https://docs.snowflake.com/en/user-guide/data-cdp-storage-costs",
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
