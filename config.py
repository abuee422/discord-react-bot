"""
Configuration module for Discord Auto-Reaction Bot.

Loads environment variables from .env file and validates required settings.
"""

import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_env_var(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """
    Get environment variable with validation.
    
    Args:
        key: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        
    Returns:
        Optional[str]: Environment variable value or default
        
    Raises:
        ValueError: If required variable is missing
    """
    value = os.getenv(key, default)
    
    if required and not value:
        raise ValueError(f"Missing required environment variable: {key}")
    
    return value


# Discord credentials and configuration
AUTH_TOKEN: Optional[str] = get_env_var("AUTH_TOKEN", required=True)
CHANNEL_ID: Optional[str] = get_env_var("CHANNEL_ID", required=True)
EMOJI: str = get_env_var("EMOJI", default="✅") or "✅"
