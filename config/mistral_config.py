import os
import logging
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
# This is primarily for local development.
load_dotenv()

# Get the Mistral API key
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Log the status of the API key (masked for security)
if MISTRAL_API_KEY:
    logger.info("MISTRAL_API_KEY loaded successfully")
    if len(MISTRAL_API_KEY) > 5:
        masked_key = f"{MISTRAL_API_KEY[:5]}...{MISTRAL_API_KEY[-3:]}"
        logger.debug(f"API Key: {masked_key} (partially masked for security)")
else:
    error_msg = "MISTRAL_API_KEY not found in environment variables. Make sure it's set in your .env file or in your hosting environment."
    logger.error(error_msg)
    # Raise an exception to prevent the application from starting without the key
    raise ValueError(error_msg)

# You can add other configuration variables here as needed.

if __name__ == "__main__":
    # Set up logging for direct execution
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # This part is for testing the configuration loading directly
    if MISTRAL_API_KEY:
        print(f"Successfully loaded MISTRAL_API_KEY: {MISTRAL_API_KEY[:5]}... (partially hidden for security)")
    else:
        print("Failed to load MISTRAL_API_KEY. Make sure it's set in your .env file or environment.") 