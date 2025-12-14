# Discord Auto-Reaction Bot

A Python-based Discord bot that automatically adds reactions to messages in a specified channel using the Discord API.

## Overview

This bot fetches the latest messages from a Discord channel and automatically reacts to each message with a specified emoji. It includes robust error handling, rate limiting, and security best practices.

## Features

- Automatic reaction to messages in a specified Discord channel
- Support for both Unicode and custom Discord emojis
- Intelligent rate limiting with automatic retry logic
- Comprehensive error handling and logging
- Input validation for all parameters
- Secure configuration using environment variables

## Requirements

- Python 3.8 or higher
- Discord bot token
- Bot must be added to your Discord server with appropriate permissions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/abuee422/discord-react-bot.git
cd discord-react-bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Discord Bot Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Navigate to the "Bot" section in the left sidebar
4. Click "Add Bot" and confirm
5. Under "Token", click "Reset Token" or "Copy" to get your bot token
6. Set the following bot permissions:
   - Read Messages/View Channels
   - Add Reactions
   - Read Message History

### Invite Bot to Server

1. Go to "OAuth2" → "URL Generator"
2. Select "bot" scope
3. Select permissions: "Read Messages", "Add Reactions", "Read Message History"
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

### Environment Variables

Create a `.env` file in the project directory:

```env
AUTH_TOKEN=your_discord_bot_token_here
CHANNEL_ID=your_target_channel_id_here
EMOJI=✅
```

**Configuration Options:**

- `AUTH_TOKEN`: Your Discord bot token (required)
- `CHANNEL_ID`: The Discord channel ID where reactions should be added (required)
- `EMOJI`: The emoji to use for reactions (default: ✅)
  - Unicode emoji: `✅`, `👍`, `❤️`
  - Custom emoji: `:emoji_name:123456789012345678` or `<:emoji_name:123456789012345678>`

### Getting Channel ID

1. Enable Developer Mode in Discord:
   - User Settings → Advanced → Enable Developer Mode
2. Right-click on the target channel
3. Select "Copy Channel ID"
4. Paste it into your `.env` file

## Usage

Run the bot:

```bash
python main.py
```

The bot will:
1. Load configuration from `.env` file
2. Validate all settings
3. Fetch the latest messages from the specified channel (up to 100)
4. React to each message with the specified emoji
5. Display detailed logs in the terminal

## Troubleshooting

**Bot does not react to messages:**
- Verify the bot has Read Messages, View Channels, and Add Reactions permissions
- Ensure the bot is in the server and has access to the channel
- Check that `AUTH_TOKEN` and `CHANNEL_ID` in `.env` are correct
- Review logs for specific error messages

**Authentication errors:**
- Ensure you are using a bot token, not a user token
- Verify the token has not been reset or revoked
- Check that the token is correctly set in `.env` (no extra spaces or quotes)

**Rate limit errors:**
- The bot automatically handles rate limits with retry logic
- Default delay is 1 second between reactions
- Persistent rate limits will trigger automatic wait and retry

**Channel not found:**
- Verify the channel ID is correct (17-19 digit number)
- Ensure the bot has access to the channel
- Check that the channel exists and has not been deleted

**Permission errors:**
- Verify the bot has required permissions in the channel
- Check server and channel permission settings
- Ensure the bot role has appropriate permissions

## Security

- Never commit your `.env` file (already in `.gitignore`)
- Never share your bot token
- Use a bot token, not a user token
- Rotate tokens if compromised
- Use environment variables, never hardcode tokens in source code

## Technical Details

- Discord API Version: v10
- Rate Limiting: Automatic with exponential backoff
- Retry Logic: Up to 3 retries for transient errors
- Error Handling: Comprehensive with detailed logging
- Input Validation: All parameters validated before API calls

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome. Please ensure all code follows the existing style and includes appropriate error handling.
