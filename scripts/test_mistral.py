#!/usr/bin/env python
"""
Test script for the Mistral AI integration.
This script tests the ability to connect to the Mistral API and generate SQL from natural language.
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
logger = logging.getLogger("test_mistral")

# Import our modules
from config.mistral_config import MISTRAL_API_KEY
from query_generation.query_generator import QueryGenerator
from query_generation.sql_validator import SQLValidator

def test_mistral_api():
    """Test the Mistral AI API integration."""
    logger.info("Testing Mistral AI API integration")
    
    try:
        # Initialize the QueryGenerator
        logger.info("Initializing QueryGenerator")
        query_generator = QueryGenerator()
        
        # Test the natural language detection
        test_queries = [
            "SELECT * FROM Users",  # SQL
            "What are the top 5 products by price?",  # Natural language
            "Show me all users in New York",  # Natural language
        ]
        
        for query in test_queries:
            is_nl = query_generator.is_natural_language(query)
            logger.info(f"Query: '{query}' - Is natural language? {is_nl}")
        
        # Test SQL generation for a natural language query
        nl_query = "What are the top 5 products by price?"
        logger.info(f"Generating SQL for natural language query: '{nl_query}'")
        
        sql_query, metadata = query_generator.generate_sql_from_natural_language(nl_query)
        
        logger.info(f"Generated SQL: {sql_query}")
        logger.info(f"Metadata: {metadata}")
        
        # Test SQL validation
        logger.info("Testing SQL validation")
        sql_validator = SQLValidator()
        
        is_valid, validation_results = sql_validator.validate_query(sql_query)
        
        logger.info(f"SQL validation: Is valid? {is_valid}")
        logger.info(f"Validation results: {validation_results}")
        
        # If we got here, the test was successful
        logger.info("✅ Test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    success = test_mistral_api()
    sys.exit(0 if success else 1) 