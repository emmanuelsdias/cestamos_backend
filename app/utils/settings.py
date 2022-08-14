from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "cestamos_backend"
    bucket: str = "full_software_developers_group"
    prefix: str = "python/fast-api"
    temp_folder: str = "/home/vscode/temp"
    s3_output_path: str = "s3://athena-logs-develop/"
    cestamos_db: str = "cestamos_db"

    class Config:
        env_file = "app/.env"