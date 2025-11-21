"""
Configuration management for the ToDo List application.

This module handles loading configuration from environment variables.
"""

import os
from typing import Optional


class Config:
    """Configuration manager for the application."""

    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration from environment variables.

        Args:
            env_file: Path to .env file. If None, looks for .env in current directory.
        """
        if env_file:
            # Load specific env file
            from dotenv import load_dotenv
            load_dotenv(env_file)
        else:
            # Try to load .env from current directory
            env_path = os.path.join(os.getcwd(), '.env')
            if os.path.exists(env_path):
                from dotenv import load_dotenv
                load_dotenv(env_path)

        self.max_projects = self._get_int_env('MAX_NUMBER_OF_PROJECTS', 10)
        self.max_tasks = self._get_int_env('MAX_NUMBER_OF_TASKS', 100)
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_port = int(os.getenv('DB_PORT', 5432))
        self.db_name = os.getenv('DB_NAME', 'todo_db')
        self.db_user = os.getenv('DB_USER', 'todo_user')
        self.db_password = os.getenv('DB_PASSWORD', 'todo_pass')
        self.database_url = os.getenv(
            'DATABASE_URL',
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    def _get_int_env(self, key: str, default: int) -> int:
        """Get integer value from environment variable."""
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            print(f"Warning: Invalid value for {key}: {value}. Using default: {default}")
            return default


# Global configuration instance
config = Config()
