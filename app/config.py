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
        """Neon entrega la URL como postgresql://; SQLAlchemy necesita el driver en el nombre."""  
        if self.database_url.startswith("postgresql://"):
            return self.database_url.replace("postgresql://", "postgresql+psycopg://", 1)
        return self.database_url

settings = Settings()
