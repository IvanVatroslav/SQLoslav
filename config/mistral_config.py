import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
# This is primarily for local development.
load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    # In a real application, you might raise an error or log a warning.
    # For now, we'll print a message.
    print("Warning: MISTRAL_API_KEY not found in environment variables.")
    # You could also set a default or raise an exception:
    # raise ValueError("MISTRAL_API_KEY not found. Please set it in your .env file or environment variables.")

# You can add other configuration variables here as needed.

if __name__ == "__main__":
    # This part is for testing the configuration loading directly
    if MISTRAL_API_KEY:
        print(f"Successfully loaded MISTRAL_API_KEY: {MISTRAL_API_KEY[:5]}... (partially hidden for security)")
    else:
        print("Failed to load MISTRAL_API_KEY. Make sure it's set in your .env file or environment.") 