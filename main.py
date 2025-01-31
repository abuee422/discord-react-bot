import requests
import time
from config import *

# Discord API base URL
BASE_URL = "https://discord.com/api/v9"

# Headers for API requests
HEADERS = {
    "Authorization": AUTH_TOKEN,
    "Content-Type": "application/json",
}

def get_messages(channel_id, limit=100):
    """
    Fetch messages from a channel.
    """
    url = f"{BASE_URL}/channels/{channel_id}/messages?limit={limit}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch messages: {response.status_code} - {response.text}")
        return []

def add_reaction(channel_id, message_id, emoji):
    """
    Add a reaction to a message.
    """
    # URL-encode the emoji if necessary
    encoded_emoji = requests.utils.quote(emoji)
    url = f"{BASE_URL}/channels/{channel_id}/messages/{message_id}/reactions/{encoded_emoji}/%40me?location=Message&type=0"
    response = requests.put(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"Reacted with {emoji} to message {message_id}.")
    else:
        print(f"Failed to react to message {message_id}: {response.status_code} - {response.text}")

def add_reactions(channel_id, message_ids, emoji):
    """
    Add reactions to a list of messages.
    """
    for message_id in message_ids:
        add_reaction(channel_id, message_id, emoji)
        time.sleep(1)  # Add a delay to avoid rate limits

def main():
    # Debugging: Print token and channel ID
    print(f"Using token: {AUTH_TOKEN}")
    print(f"Using channel ID: {CHANNEL_ID}")

    try:
        # Fetch the latest messages from the channel
        messages = get_messages(CHANNEL_ID)
        if not messages:
            print("No messages found.")
            return

        # Extract message IDs (newest to oldest)
        message_ids = [msg["id"] for msg in messages]

        # Add reactions to the messages
        add_reactions(CHANNEL_ID, message_ids, EMOJI)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
