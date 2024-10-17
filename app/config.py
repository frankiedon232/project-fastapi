from pydantic_settings import BaseSettings


# Settings up environment
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secrete_key: str
    algorithms: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
