import os

# Default settings
DEFAULT_LLM_PROVIDER = "mistral"
DEFAULT_DB_SCHEMA = "star_dwh"
DEFAULT_MISTRAL_MODEL = "mistral-small-latest" # Or your currently used model

# Environment variable names for API keys
# The actual keys should be set in your environment (e.g., Render secrets)
MISTRAL_API_KEY_ENV_VAR = "MISTRAL_API_KEY"

class AppConfig:
    """
    Application configuration class.
    Loads settings from environment variables or uses defaults.
    """
    def __init__(self):
        self.llm_provider_name: str = os.getenv("LLM_PROVIDER", DEFAULT_LLM_PROVIDER)
        self.db_schema_name: str = os.getenv("DB_SCHEMA", DEFAULT_DB_SCHEMA)
        
        # LLM specific settings
        self.mistral_api_key: str | None = os.getenv(MISTRAL_API_KEY_ENV_VAR)
        self.mistral_model: str = os.getenv("MISTRAL_MODEL", DEFAULT_MISTRAL_MODEL)

        if self.llm_provider_name == "mistral" and not self.mistral_api_key:
            # This check could be done when the Mistral provider is instantiated
            # For now, QueryGenerator already has a similar check.
            pass # Or raise an error: raise ValueError(f"{MISTRAL_API_KEY_ENV_VAR} not set for Mistral provider")

# Global config instance
# Other parts of the application can import this instance
config = AppConfig()

# Example of how to access config values:
# from core.config import config
# print(config.llm_provider_name)
# print(config.db_schema_name)

if __name__ == "__main__":
    # For testing the config loader
    print(f"LLM Provider: {config.llm_provider_name}")
    print(f"DB Schema: {config.db_schema_name}")
    print(f"Mistral API Key Loaded: {'Yes' if config.mistral_api_key else 'No (will be checked by provider)'}")
    print(f"Mistral Model: {config.mistral_model}") 