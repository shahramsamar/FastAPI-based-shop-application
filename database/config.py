# Import BaseSettings from pydantic_settings, which helps manage configurations with environment variables.
from pydantic_settings import BaseSettings

# Define a Settings class that inherits from BaseSettings.
# This class will load configuration values from environment variables or use the provided defaults.
class Settings(BaseSettings):
    # Define the DATABASE_URL attribute with a default value for an SQLite database.
    # This attribute can be overridden by setting an environment variable with the same name.
    DATABASE_URL: str = "sqlite:///./shop.db"

# Instantiate the Settings class.
# This creates a settings object that loads the configuration from environment variables or defaults.
settings = Settings()
