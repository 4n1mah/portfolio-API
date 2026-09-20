from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración leída de variables de entorno (o del archivo .env en local)."""

    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "sqlite:///./local.db"

    allowed_origins: str = "http://localhost:3000,https://sadielrojas.vercel.app"

    @property
    def origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    @property
    def sqlalchemy_url(self) -> str:
        """Limpia la URL y le agrega el driver: sin eso SQLAlchemy busca psycopg2, que no usamos."""
        url = self.database_url.strip().strip('"').strip("'")
        for prefix in ("postgresql://", "postgres://"):
            if url.startswith(prefix):
                return "postgresql+psycopg://" + url[len(prefix) :]
        return url

settings = Settings()
