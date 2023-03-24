"""Environment variables for the application."""
from pydantic import BaseSettings, Field, BaseConfig

class Settings(BaseSettings):
    """Environment variables for the application."""
    SECRET_KEY: str = Field(default_factory=lambda: "secret")
    FLASK_APP: str = Field(default_factory=lambda: "app.py")
    FLASK_ENV: str = Field(default_factory=lambda: "development")
    FLASK_DEBUG: bool =Field(default_factory=lambda: True)
    FLASK_PORT: int =Field(default_factory=lambda: 5555)
    FLASK_HOST: str =Field(default_factory=lambda: "0.0.0.0")
    STATIC_FOLDER: str = Field(default_factory=lambda: "static")
    TEMPLATES_FOLDER: str = Field(default_factory=lambda: "templates")
    TEMPLATE_AUTO_RELOAD: bool = Field(default_factory=lambda: True)
    
    class Config(BaseConfig):
        """Configuration for the environment variables."""
        env_file = ".env"
        env_file_encoding = "utf-8"