import json
import logging
from typing import Dict, Tuple

from mistralai import Mistral # Corrected import based on typical usage
# from mistralai.models.chat_completion import ChatMessage # For older versions
from mistralai.models.chat_completion import ChatMessage # Assuming this is the modern way or use mistral_models from QueryGenerator

from core.config import config # Use the new AppConfig instance
from .base import LLMProviderInterface

class MistralLLMProvider(LLMProviderInterface):
    """
    LLMProvider implementation for Mistral AI.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.model_name = config.mistral_model # Get model from global config

        if not config.mistral_api_key:
            self.logger.error("MISTRAL_API_KEY not found in environment or config.")
            raise ValueError("MISTRAL_API_KEY is required for MistralLLMProvider.")
        
        self.client = Mistral(api_key=config.mistral_api_key)
        # The schema will be passed to generate_sql or handled internally based on schema_name
        # For now, let's replicate the existing behavior by having a method for the default schema.
        self.default_schema_content = self._get_default_star_dwh_schema()

    def _get_default_star_dwh_schema(self) -> str:
        """
        Returns the hardcoded star_dwh schema.
        This is to maintain current functionality. Future versions should load this dynamically.
        """
        # This schema content is taken directly from the original QueryGenerator
        schema = """
        # This schema represents a star schema data warehouse for sales data
        
        Table: DimCustomer
        Columns: customer_key (INT, PRIMARY KEY), first_name (VARCHAR), last_name (VARCHAR), 
                email (VARCHAR), address (VARCHAR), city (VARCHAR), state (VARCHAR),
                country (VARCHAR), postal_code (VARCHAR), phone (VARCHAR),
                created_at (TIMESTAMP)

        Table: DimProduct
        Columns: product_key (INT, PRIMARY KEY), name (VARCHAR), category (VARCHAR),
                subcategory (VARCHAR), brand (VARCHAR), price_usd (DECIMAL),
                cost_usd (DECIMAL), description (TEXT)
                
        Table: DimStore
        Columns: store_key (INT, PRIMARY KEY), name (VARCHAR), 
                address (VARCHAR), city (VARCHAR), state (VARCHAR),
                country (VARCHAR), postal_code (VARCHAR), phone (VARCHAR),
                manager_name (VARCHAR), open_date (DATE)
                
        Table: DimEmployee
        Columns: employee_key (INT, PRIMARY KEY), first_name (VARCHAR), last_name (VARCHAR),
                position (VARCHAR), hire_date (DATE), salary (DECIMAL),
                store_key (INT, FOREIGN KEY to DimStore.store_key)
                
        Table: DimDate
        Columns: date_key (INT, PRIMARY KEY), full_date (DATE), 
                day_of_week (INT), day_name (VARCHAR), day_of_month (INT), 
                day_of_year (INT), week_of_year (INT), month (INT), 
                month_name (VARCHAR), quarter (INT), year (INT),
                is_weekend (BOOLEAN), is_holiday (BOOLEAN)
                
        Table: DimCurrency
        Columns: currency_key (INT, PRIMARY KEY), currency_code (VARCHAR),
                currency_name (VARCHAR), currency_rate (DECIMAL)
                
        Table: FactSales
        Columns: sales_key (BIGINT, PRIMARY KEY), 
                customer_key (INT, FOREIGN KEY to DimCustomer.customer_key),
                product_key (INT, FOREIGN KEY to DimProduct.product_key),
                store_key (INT, FOREIGN KEY to DimStore.store_key),
                employee_key (INT, FOREIGN KEY to DimEmployee.employee_key),
                date_key (INT, FOREIGN KEY to DimDate.date_key),
                currency_key (INT, FOREIGN KEY to DimCurrency.currency_key),
                hour (INT), minute (INT), quantity (INT),
                unit_price (DECIMAL), unit_price_usd (DECIMAL),
                total_price (DECIMAL), total_price_usd (DECIMAL),
                transaction_time (TIMESTAMP)
        """
        return schema.strip()

    def _build_prompt(self, question: str, schema_content: str) -> Dict[str, str]:
        """
        Builds the prompt to send to the Mistral AI model.
        """
        system_prompt = f"""
        You are an expert SQL query generator. Your task is to convert natural language questions into 
        correct and efficient SQL queries based on the provided database schema.
        
        DATABASE SCHEMA:
        {schema_content}
        
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
        (Logic moved from QueryGenerator)
        """
        self.logger.debug(f"Raw Mistral response: {response_text}")
        try:
            response_text = response_text.strip()
            if response_text.startswith("```json") and response_text.endswith("```"):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith("```") and response_text.endswith("```"):
                response_text = response_text[3:-3].strip()
            
            response_json = json.loads(response_text)
            
            if "error" in response_json:
                raise ValueError(response_json.get("message", "Unknown error in query generation"))
            
            sql_query = response_json.get("sql", "")
            metadata = {k: v for k, v in response_json.items() if k != "sql"}
            return sql_query, metadata
            
        except json.JSONDecodeError:
            self.logger.warning(f"Failed to parse JSON from response: {response_text}")
            # Fallback heuristic from QueryGenerator
            if "SELECT" in response_text.upper():
                lines = response_text.split("\n")
                sql_lines = []
                capturing = False
                for line in lines:
                    if "SELECT" in line.upper() and not capturing:
                        capturing = True
                    if capturing:
                        sql_lines.append(line)
                        if ";" in line:
                            break
                if sql_lines:
                    sql_query = "\n".join(sql_lines).strip()
                    return sql_query, {"extracted": "heuristic", "original_response": response_text}
            return response_text, {"extracted": "raw", "parse_error": "Could not extract structured SQL"}

    def generate_sql(self, natural_language_query: str, schema_name: str) -> Tuple[str, Dict]:
        self.logger.info(f"Generating SQL for question: '{natural_language_query}' using schema: '{schema_name}' with Mistral model: '{self.model_name}'")

        # For now, if schema_name is the default, use the hardcoded schema.
        # Future: Load schema dynamically based on schema_name.
        current_schema_content = ""
        if schema_name.lower() == "star_dwh": # Assuming config.db_schema_name will be 'star_dwh' by default
            current_schema_content = self.default_schema_content
        else:
            # Placeholder for handling other schemas or raising an error
            self.logger.warning(f"Schema '{schema_name}' is not the default 'star_dwh'. Dynamic schema loading not yet implemented. Using default schema.")
            current_schema_content = self.default_schema_content # Or raise NotImplementedError

        prompt_messages = self._build_prompt(natural_language_query, current_schema_content)
        
        try:
            # Using the structure from QueryGenerator's Mistral call
            # Note: The original QueryGenerator used self.client.chat.complete(...)
            # The MistralClient might be initialized as `self.client = Mistral(...)` and then `self.client.chat(...)`
            # Or, if `Mistral` from `mistralai` is the client itself, then `self.client.chat.completions.create(...)`
            # Let's assume `MistralClient` is the correct top-level client from `mistralai.client`
            # and the API is `self.client.chat(...)` as per newer SDK versions or `self.client.chat.completions.create(...)`
            
            # Based on the original QG: `response = self.client.chat.complete(` - this seems like a custom wrapper or older SDK.
            # The standard Mistral Python client `mistralai.MistralClient` uses `client.chat(...)`.
            # Let's stick to what seems more standard:
            chat_response = self.client.chat(
                model=self.model_name,
                messages=[
                    ChatMessage(role="system", content=prompt_messages["system"]),
                    ChatMessage(role="user", content=prompt_messages["user"])
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            # Check if response.choices is non-empty and message.content exists
            if not chat_response.choices or not chat_response.choices[0].message or not chat_response.choices[0].message.content:
                self.logger.error("Mistral API response is empty or malformed.")
                raise RuntimeError("Mistral API response is empty or malformed.")

            sql_query, metadata = self._extract_sql_from_response(chat_response.choices[0].message.content)
            
            # Add model name to metadata for clarity
            metadata['llm_provider'] = 'mistral'
            metadata['model_name'] = self.model_name
            metadata['schema_used'] = schema_name

            self.logger.info(f"Generated SQL query: {sql_query}")
            return sql_query, metadata
            
        except Exception as e:
            self.logger.error(f"Error calling Mistral AI API: {str(e)}", exc_info=True)
            # Propagate a more specific error or the original one
            raise RuntimeError(f"MistralLLMProvider failed to generate SQL query: {str(e)}")


    def is_natural_language(self, text: str) -> bool:
        """
        Determines if the input is likely natural language rather than SQL.
        (Logic moved from QueryGenerator)
        """
        # Simple heuristic: if it doesn't contain common SQL keywords, it's likely natural language.
        # This heuristic is case-insensitive.
        sql_keywords = [
            "SELECT", "FROM", "WHERE", "INSERT", "UPDATE", "DELETE", "CREATE", 
            "ALTER", "DROP", "TABLE", "JOIN", "GROUP BY", "ORDER BY", "LIMIT",
            "OFFSET", "HAVING", "UNION", "VALUES", "INDEX", "VIEW", "TRIGGER",
            "PROCEDURE", "FUNCTION", "DATABASE", "SCHEMA" 
        ]
        text_upper = text.upper()
        
        # Check for specific patterns that are clearly SQL
        if text_upper.strip().startswith("EXPLAIN ") or text_upper.strip().startswith("DESCRIBE "):
            return False # These are usually SQL commands

        # Check for SQL comments
        if text.strip().startswith("--") or text.strip().startswith("/*"):
            return False

        # Check for presence of multiple SQL keywords
        found_keywords = 0
        for keyword in sql_keywords:
            if keyword in text_upper:
                found_keywords +=1
        
        # If very few or no SQL keywords, likely natural language
        # If more, it's likely SQL or mixed. This threshold can be tuned.
        # A simple approach: if common SQL starting words are present, it's likely SQL.
        common_sql_starters = ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP", "WITH"]
        for starter in common_sql_starters:
            if text_upper.startswith(starter):
                return False
        
        # If no strong SQL signals, assume natural language.
        # The original heuristic was: `not any(keyword in text_upper for keyword in sql_keywords)`
        # Let's refine slightly: if it contains a few SQL keywords AND starts like one, it's SQL.
        # Otherwise, more likely NL.
        
        # Let's stick to the original simple and effective heuristic for now to ensure no behavior change:
        original_sql_keywords = ["SELECT", "FROM", "WHERE", "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP", "TABLE", "JOIN"]
        if any(keyword in text_upper for keyword in original_sql_keywords):
            # It contains at least one major SQL keyword.
            # Further check: does it *primarily* look like SQL?
            # A simple check: if it contains ';', it's highly likely SQL.
            if ';' in text:
                return False
            # If it has several SQL keywords and not too many other words, it might be SQL.
            # This gets complex. The original heuristic is safer for now.
            # `return not any(keyword in text_upper for keyword in sql_keywords)` implies that if ANY keyword is found, it's NOT NL.
            # This might be too strict. Example: "Show me sales FROM last month" would be SQL.
            # The original `QueryGenerator` code read:
            # `return not any(keyword in text_upper for keyword in sql_keywords)`
            # This means: if any SQL keyword is found, `any(...)` is true, `not any(...)` is false. So it's considered SQL.
            # If NO SQL keyword is found, `any(...)` is false, `not any(...)` is true. So it's considered NL.
            # This seems correct for the original intent.
            return False # It contains SQL keywords, so it's likely SQL or mixed. Treat as SQL for safety.

        return True # No common SQL keywords found, assume Natural Language. 