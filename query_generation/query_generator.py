import json
import logging
from typing import Dict, Optional, Tuple, Union

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from config.mistral_config import MISTRAL_API_KEY


class QueryGenerator:
    """
    Handles natural language processing and conversion to SQL queries
    using the Mistral AI API.
    """

    def __init__(self, mistral_model: str = "mistral-large-latest"):
        """
        Initialize the QueryGenerator.

        Args:
            mistral_model: The Mistral AI model to use for query generation.
        """
        if not MISTRAL_API_KEY:
            raise ValueError("MISTRAL_API_KEY not found. Please set it in your .env file.")
        
        self.client = MistralClient(api_key=MISTRAL_API_KEY)
        self.model = mistral_model
        self.logger = logging.getLogger(__name__)
        
        # In a more advanced implementation, this would be loaded from a database
        # or configuration file. For this first phase, we'll hardcode a sample schema.
        self.schema = self._get_sample_schema()
    
    def _get_sample_schema(self) -> str:
        """
        Returns a sample database schema as a string.
        This is a simplified version for initial testing.
        
        Returns:
            A string representation of the database schema.
        """
        schema = """
        Table: Users
        Columns: user_id (INT, PRIMARY KEY), name (VARCHAR), city (VARCHAR), 
                email (VARCHAR), signup_date (DATE), last_login (TIMESTAMP)

        Table: Products
        Columns: product_id (INT, PRIMARY KEY), name (VARCHAR), category (VARCHAR),
                price (DECIMAL), description (TEXT), created_at (TIMESTAMP)
                
        Table: Orders
        Columns: order_id (INT, PRIMARY KEY), user_id (INT, FOREIGN KEY to Users.user_id),
                order_date (DATE), total_amount (DECIMAL), status (VARCHAR)
                
        Table: OrderItems
        Columns: item_id (INT, PRIMARY KEY), order_id (INT, FOREIGN KEY to Orders.order_id),
                product_id (INT, FOREIGN KEY to Products.product_id), quantity (INT),
                price (DECIMAL)
        """
        return schema.strip()

    def generate_sql_from_natural_language(self, question: str) -> Tuple[str, Dict]:
        """
        Takes a natural language question and generates a SQL query.
        
        Args:
            question: A natural language question about the database.
            
        Returns:
            A tuple containing the generated SQL query and additional metadata.
        """
        self.logger.info(f"Generating SQL for question: {question}")
        
        # Construct the prompt for the Mistral AI model
        prompt = self._build_prompt(question)
        
        try:
            # Call the Mistral AI API
            response = self.client.chat(
                messages=[
                    ChatMessage(role="system", content=prompt["system"]),
                    ChatMessage(role="user", content=prompt["user"])
                ],
                model=self.model,
                temperature=0.1,  # Low temperature for more deterministic responses
                max_tokens=1000
            )
            
            # Extract the SQL query from the response
            sql_query, metadata = self._extract_sql_from_response(response.choices[0].message.content)
            
            self.logger.info(f"Generated SQL query: {sql_query}")
            return sql_query, metadata
            
        except Exception as e:
            self.logger.error(f"Error calling Mistral AI API: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to generate SQL query: {str(e)}")
    
    def _build_prompt(self, question: str) -> Dict[str, str]:
        """
        Builds the prompt to send to the Mistral AI model.
        
        Args:
            question: The natural language question.
            
        Returns:
            A dictionary containing the system and user prompts.
        """
        system_prompt = f"""
        You are an expert SQL query generator. Your task is to convert natural language questions into 
        correct and efficient SQL queries based on the provided database schema.
        
        DATABASE SCHEMA:
        {self.schema}
        
        INSTRUCTIONS:
        1. Generate a valid SQL query that answers the user's question.
        2. Only use tables and columns that exist in the schema.
        3. Format your response in JSON with two fields:
           - "sql": The generated SQL query
           - "explanation": A brief explanation of what the query does
        4. Do not include any text outside of the JSON structure.
        5. If you can't generate a query due to ambiguity or missing information, 
           return a JSON with "error" and "message" fields explaining the issue.
        """
        
        user_prompt = f"Convert this question to SQL: {question}"
        
        return {
            "system": system_prompt.strip(),
            "user": user_prompt
        }
    
    def _extract_sql_from_response(self, response_text: str) -> Tuple[str, Dict]:
        """
        Extracts the SQL query from the Mistral AI response.
        
        Args:
            response_text: The text response from Mistral AI.
            
        Returns:
            A tuple containing the SQL query string and additional metadata.
        """
        self.logger.debug(f"Raw Mistral response: {response_text}")
        
        # Try to extract JSON from the response
        try:
            # Look for JSON-like content and extract it
            response_text = response_text.strip()
            
            # If the response is wrapped in triple backticks, extract the content
            if response_text.startswith("```json") and response_text.endswith("```"):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith("```") and response_text.endswith("```"):
                response_text = response_text[3:-3].strip()
            
            # Parse the JSON
            response_json = json.loads(response_text)
            
            # If there's an error in the response, raise it
            if "error" in response_json:
                raise ValueError(response_json.get("message", "Unknown error in query generation"))
            
            # Extract the SQL query and any metadata
            sql_query = response_json.get("sql", "")
            
            # Return the SQL query and additional metadata
            metadata = {k: v for k, v in response_json.items() if k != "sql"}
            return sql_query, metadata
            
        except json.JSONDecodeError:
            self.logger.warning(f"Failed to parse JSON from response: {response_text}")
            # If we couldn't parse JSON, try to extract SQL directly using heuristics
            
            # Look for SQL keywords
            if "SELECT" in response_text.upper():
                # Extract the SQL query using simple heuristics
                lines = response_text.split("\n")
                sql_lines = []
                capturing = False
                
                for line in lines:
                    if "SELECT" in line.upper() and not capturing:
                        capturing = True
                    
                    if capturing:
                        sql_lines.append(line)
                        
                        # Stop capturing when we reach the end of the SQL query
                        if ";" in line:
                            break
                
                if sql_lines:
                    sql_query = "\n".join(sql_lines).strip()
                    return sql_query, {"extracted": "heuristic", "original_response": response_text}
            
            # If we still couldn't extract SQL, return the entire response as is
            return response_text, {"extracted": "raw", "parse_error": "Could not extract structured SQL"}
    
    def is_natural_language(self, text: str) -> bool:
        """
        Determines if the input is likely natural language rather than SQL.
        
        Args:
            text: The input text to analyze.
            
        Returns:
            True if the text is likely natural language, False if it's likely SQL.
        """
        # Simple heuristic: Check if the text starts with common SQL keywords
        sql_starters = ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP", "WITH"]
        
        # Normalize the text for comparison
        normalized_text = text.strip().upper()
        
        # Check if it starts with any SQL keyword
        for starter in sql_starters:
            if normalized_text.startswith(starter):
                return False
        
        # If it doesn't start with SQL keywords, it's likely natural language
        return True 