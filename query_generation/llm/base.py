from abc import ABC, abstractmethod
from typing import Tuple, Dict

class LLMProviderInterface(ABC):
    """
    Interface for LLM providers to generate SQL from natural language
    and determine if a given text is natural language.
    """

    @abstractmethod
    def generate_sql(self, natural_language_query: str, schema_name: str) -> Tuple[str, Dict]:
        """
        Generates an SQL query from a natural language query, targeting a specific schema.

        Args:
            natural_language_query: The user's question in natural language.
            schema_name: The name of the database schema to target.

        Returns:
            A tuple containing the generated SQL query string and a dictionary of metadata.
        """
        pass

    @abstractmethod
    def is_natural_language(self, text: str) -> bool:
        """
        Determines if the given text is likely natural language or an SQL query.

        Args:
            text: The input text to analyze.

        Returns:
            True if the text is considered natural language, False otherwise.
        """
        pass 