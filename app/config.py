from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración leída de variables de entorno (o del archivo .env en local)."""

    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "sqlite:///./local.db"

    allowed_origins: str = "http://localhost:3000,https://sadielrojas.vercel.app"

    @property
    def origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]


settings = Settings()
