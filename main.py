"""
Discord Auto-Reaction Bot

A bot that automatically reacts to messages in a specified Discord channel.
Uses the Discord API with proper error handling, rate limiting, and security practices.
"""

import logging
import time
import re
from typing import List, Dict, Optional
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import AUTH_TOKEN, CHANNEL_ID, EMOJI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Discord API configuration
BASE_URL = "https://discord.com/api/v10"
DEFAULT_RATE_LIMIT_DELAY = 1.0  # seconds between requests
MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 2


def get_headers() -> Dict[str, str]:
    """
    Get request headers with authentication token.
    
    Returns:
        Dict[str, str]: Headers dictionary
        
    Raises:
        ValueError: If AUTH_TOKEN is not set
    """
    if not AUTH_TOKEN:
        raise ValueError("AUTH_TOKEN is not set. Please check your .env file.")
    
    return {
        "Authorization": AUTH_TOKEN,
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (discord-react-bot, 1.0)",
    }


def create_session() -> requests.Session:
    """
    Create a requests session with retry strategy for handling rate limits and transient errors.
    
    Returns:
        requests.Session: Configured session with retry adapter
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=RETRY_BACKOFF_FACTOR,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "PUT"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def validate_channel_id(channel_id: str) -> bool:
    """
    Validate Discord channel ID format.
    
    Args:
        channel_id: The channel ID to validate
        
    Returns:
        bool: True if valid format, False otherwise
    """
    # Discord IDs are 17-19 digit numbers
    return bool(re.match(r'^\d{17,19}$', channel_id))


def validate_emoji(emoji: str) -> bool:
    """
    Validate emoji format (unicode emoji or custom emoji format).
    
    Args:
        emoji: The emoji string to validate
        
    Returns:
        bool: True if valid format, False otherwise
    """
    # Unicode emoji or custom emoji format (name:id)
    return bool(emoji and (len(emoji) > 0))


def encode_emoji(emoji: str) -> str:
    """
    Properly encode emoji for Discord API URL.
    
    Args:
        emoji: The emoji to encode (unicode or custom format)
        
    Returns:
        str: URL-encoded emoji string
    """
    # Custom emojis are in format "name:id", unicode emojis are just the emoji
    if ':' in emoji and emoji.count(':') == 2:
        # Custom emoji format: <:name:id> or :name:id:
        # Extract name:id part
        emoji_clean = emoji.strip('<>:')
        return quote(emoji_clean, safe='')
    else:
        # Unicode emoji - encode it
        return quote(emoji, safe='')


def get_messages(channel_id: str, limit: int = 100, session: Optional[requests.Session] = None) -> List[Dict]:
    """
    Fetch messages from a Discord channel.
    
    Args:
        channel_id: The Discord channel ID
        limit: Maximum number of messages to fetch (1-100)
        session: Optional requests session (creates new if not provided)
        
    Returns:
        List[Dict]: List of message objects, empty list on error
    """
    if not validate_channel_id(channel_id):
        logger.error(f"Invalid channel ID format: {channel_id}")
        return []
    
    if not (1 <= limit <= 100):
        logger.warning(f"Limit {limit} out of range, using 100")
        limit = 100
    
    url = f"{BASE_URL}/channels/{channel_id}/messages"
    params = {"limit": limit}
    
    if session is None:
        session = create_session()
    
    try:
        headers = get_headers()
        response = session.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            messages = response.json()
            logger.info(f"Successfully fetched {len(messages)} messages from channel {channel_id}")
            return messages
        elif response.status_code == 401:
            logger.error("Authentication failed. Check your AUTH_TOKEN.")
            return []
        elif response.status_code == 403:
            logger.error("Forbidden. Bot may lack required permissions (Read Messages, View Channel).")
            return []
        elif response.status_code == 404:
            logger.error(f"Channel {channel_id} not found or bot doesn't have access.")
            return []
        elif response.status_code == 429:
            retry_after = response.headers.get('Retry-After', DEFAULT_RATE_LIMIT_DELAY)
            logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
            time.sleep(float(retry_after))
            return get_messages(channel_id, limit, session)  # Retry
        else:
            logger.error(f"Failed to fetch messages: {response.status_code} - {response.text}")
            return []
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while fetching messages: {e}")
        return []
    except ValueError as e:
        logger.error(f"Invalid JSON response: {e}")
        return []


def add_reaction(
    channel_id: str,
    message_id: str,
    emoji: str,
    session: Optional[requests.Session] = None
) -> bool:
    """
    Add a reaction to a Discord message.
    
    Args:
        channel_id: The Discord channel ID
        message_id: The message ID to react to
        emoji: The emoji to use (unicode or custom format)
        session: Optional requests session (creates new if not provided)
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not validate_channel_id(channel_id):
        logger.error(f"Invalid channel ID format: {channel_id}")
        return False
    
    if not validate_emoji(emoji):
        logger.error(f"Invalid emoji format: {emoji}")
        return False
    
    # Validate message ID format
    if not re.match(r'^\d{17,19}$', message_id):
        logger.error(f"Invalid message ID format: {message_id}")
        return False
    
    encoded_emoji = encode_emoji(emoji)
    # Correct Discord API endpoint: PUT /channels/{channel.id}/messages/{message.id}/reactions/{emoji}/@me
    url = f"{BASE_URL}/channels/{channel_id}/messages/{message_id}/reactions/{encoded_emoji}/@me"
    
    if session is None:
        session = create_session()
    
    try:
        headers = get_headers()
        response = session.put(url, headers=headers, timeout=10)
        
        if response.status_code == 204:
            logger.info(f"Successfully reacted with {emoji} to message {message_id}")
            return True
        elif response.status_code == 401:
            logger.error("Authentication failed. Check your AUTH_TOKEN.")
            return False
        elif response.status_code == 403:
            logger.warning(f"Permission denied. Bot may lack 'Add Reactions' permission for message {message_id}")
            return False
        elif response.status_code == 404:
            logger.warning(f"Message {message_id} not found or already deleted")
            return False
        elif response.status_code == 429:
            retry_after = response.headers.get('Retry-After', DEFAULT_RATE_LIMIT_DELAY)
            logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
            time.sleep(float(retry_after))
            return add_reaction(channel_id, message_id, emoji, session)  # Retry
        else:
            logger.error(f"Failed to react to message {message_id}: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while adding reaction: {e}")
        return False


def add_reactions(channel_id: str, message_ids: List[str], emoji: str, delay: float = DEFAULT_RATE_LIMIT_DELAY) -> Dict[str, int]:
    """
    Add reactions to multiple messages with rate limiting.
    
    Args:
        channel_id: The Discord channel ID
        message_ids: List of message IDs to react to
        emoji: The emoji to use
        delay: Delay between reactions in seconds
        
    Returns:
        Dict[str, int]: Statistics with 'success' and 'failed' counts
    """
    if not message_ids:
        logger.warning("No message IDs provided")
        return {"success": 0, "failed": 0}
    
    stats = {"success": 0, "failed": 0}
    session = create_session()
    
    logger.info(f"Starting to add reactions to {len(message_ids)} messages...")
    
    for idx, message_id in enumerate(message_ids, 1):
        if add_reaction(channel_id, message_id, emoji, session):
            stats["success"] += 1
        else:
            stats["failed"] += 1
        
        # Add delay between reactions (except for the last one)
        if idx < len(message_ids):
            time.sleep(delay)
    
    logger.info(f"Reaction process complete: {stats['success']} succeeded, {stats['failed']} failed")
    return stats


def main() -> None:
    """
    Main function to run the Discord auto-reaction bot.
    """
    logger.info("Starting Discord Auto-Reaction Bot")
    logger.info(f"Target channel ID: {CHANNEL_ID}")
    logger.info(f"Using emoji: {EMOJI}")
    # Security: Do NOT log the token
    
    try:
        # Validate configuration
        if not AUTH_TOKEN:
            logger.error("AUTH_TOKEN is not set. Please check your .env file.")
            return
        
        if not CHANNEL_ID:
            logger.error("CHANNEL_ID is not set. Please check your .env file.")
            return
        
        if not EMOJI:
            logger.error("EMOJI is not set. Please check your .env file.")
            return
        
        # Fetch the latest messages from the channel
        messages = get_messages(CHANNEL_ID)
        
        if not messages:
            logger.warning("No messages found or failed to fetch messages.")
            return
        
        # Extract message IDs (newest to oldest)
        message_ids = [msg.get("id") for msg in messages if msg.get("id")]
        
        if not message_ids:
            logger.warning("No valid message IDs found in fetched messages.")
            return
        
        logger.info(f"Found {len(message_ids)} messages to react to")
        
        # Add reactions to the messages
        stats = add_reactions(CHANNEL_ID, message_ids, EMOJI)
        
        logger.info(f"Bot execution completed successfully. Stats: {stats}")
        
    except KeyboardInterrupt:
        logger.info("Bot execution interrupted by user")
    except Exception as e:
        logger.exception(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
