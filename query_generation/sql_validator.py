import logging
import re
from typing import Dict, Tuple, Union


class SQLValidator:
    """
    Validates SQL queries for syntax correctness and security issues.
    This is a simple implementation for Phase 1, which will be enhanced over time.
    """
    
    def __init__(self):
        """
        Initialize the SQL validator with basic validation rules.
        """
        self.logger = logging.getLogger(__name__)
        
        # List of potentially dangerous SQL operations that should be blocked
        self.dangerous_operations = [
            r"\bDROP\s+",
            r"\bTRUNCATE\s+",
            r"\bDELETE\s+FROM\s+",
            r"\bALTER\s+TABLE\s+",
            r"\bUPDATE\s+",
            r"\bINSERT\s+INTO\s+",
            r";\s*DROP\s+",  # Prevent SQL injection with multiple statements
            r"--",  # SQL comment that could be used for injection
            r"/\*"  # Multi-line comment that could be used for injection
        ]
        
        # For Phase 1, we'll only allow SELECT statements
        self.allowed_operations = [
            r"\bSELECT\s+"
        ]
    
    def validate_query(self, sql_query: str) -> Tuple[bool, Dict[str, Union[bool, str]]]:
        """
        Validates a SQL query for syntax and security issues.
        
        Args:
            sql_query: The SQL query to validate.
            
        Returns:
            A tuple with:
            - Boolean indicating if the query is valid
            - Dictionary with validation details
        """
        self.logger.info(f"Validating query: {sql_query}")
        
        validation_result = {
            "is_valid": True,
            "issues": []
        }
        
        # Check if the query is empty
        if not sql_query or not sql_query.strip():
            validation_result["is_valid"] = False
            validation_result["issues"].append("Empty query")
            return False, validation_result
        
        # Check for allowed operations (for Phase 1, only SELECT is allowed)
        allowed = False
        for pattern in self.allowed_operations:
            if re.search(pattern, sql_query, re.IGNORECASE):
                allowed = True
                break
        
        if not allowed:
            validation_result["is_valid"] = False
            validation_result["issues"].append("Only SELECT queries are allowed in this phase")
            return False, validation_result
        
        # Check for dangerous operations
        for pattern in self.dangerous_operations:
            if re.search(pattern, sql_query, re.IGNORECASE):
                validation_result["is_valid"] = False
                validation_result["issues"].append(f"Potentially dangerous operation detected: {pattern}")
                return False, validation_result
        
        # Basic syntax check
        if not self._check_basic_syntax(sql_query):
            validation_result["is_valid"] = False
            validation_result["issues"].append("Basic syntax check failed")
            return False, validation_result
        
        self.logger.info("Query passed validation")
        return True, validation_result
    
    def _check_basic_syntax(self, sql_query: str) -> bool:
        """
        Performs a basic syntax check on the SQL query.
        This is a simplified check for Phase 1.
        
        Args:
            sql_query: The SQL query to check.
            
        Returns:
            Boolean indicating if the query's basic syntax is valid.
        """
        # In a production system, you might use a SQL parser library here,
        # but for Phase 1 we'll do some basic checks
        
        # Check for balanced parentheses
        if sql_query.count('(') != sql_query.count(')'):
            self.logger.warning("Unbalanced parentheses in query")
            return False
        
        # Check for semicolon at the end (or not in the middle)
        semicolons = sql_query.count(';')
        if semicolons > 1 or (semicolons == 1 and not sql_query.rstrip().endswith(';')):
            self.logger.warning("Improper semicolon usage in query")
            return False
        
        # Check for basic SELECT structure (very simplified)
        if sql_query.upper().startswith('SELECT'):
            # Very basic check: should have FROM after SELECT
            if 'FROM' not in sql_query.upper():
                self.logger.warning("SELECT query missing FROM clause")
                return False
        
        return True 