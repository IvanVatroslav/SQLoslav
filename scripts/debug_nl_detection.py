#!/usr/bin/env python
"""
Debug utility for the natural language detection.
This script tests whether a message would be detected as natural language or SQL.
"""

import logging
import os
import sys

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("debug_nl_detection")

# Import the QueryGenerator class
from query_generation.query_generator import QueryGenerator

def debug_nl_detection(message):
    """
    Debug natural language detection for a given message.
    
    Args:
        message: The message text to test.
    """
    logger.info(f"Debugging natural language detection for message: {message}")
    
    # If the message starts with 'SQLoslav', extract the actual text
    if message.startswith("SQLoslav"):
        lines = message.strip().split("\n")
        if len(lines) > 1:
            actual_text = "\n".join(lines[1:])
            logger.info(f"Extracted text: {actual_text}")
        else:
            logger.error("Invalid message format - expected multiple lines")
            return
    else:
        actual_text = message
    
    # Initialize the QueryGenerator
    query_generator = QueryGenerator()
    
    # Test if the text is natural language
    is_natural_language = query_generator.is_natural_language(actual_text)
    
    logger.info(f"Is natural language? {is_natural_language}")
    logger.info(f"Would be processed as: {'Natural Language' if is_natural_language else 'SQL'}")
    
    # Print SQL keyword checks
    for keyword in query_generator.sql_starters:
        if actual_text.strip().upper().startswith(keyword):
            logger.info(f"Matched SQL keyword: {keyword}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If message is provided as command line argument
        debug_nl_detection(sys.argv[1])
    else:
        # Interactive mode
        print("Enter messages to test natural language detection (Ctrl+C to exit):")
        try:
            while True:
                message = input("> ")
                debug_nl_detection(message)
                print()
        except KeyboardInterrupt:
            print("\nExiting.") 