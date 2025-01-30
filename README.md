## Discord Auto-Reaction Bot

### Overview
This is a simple bot that automatically reacts to the latest messages in a specified Discord channel. The bot interacts with the Discord API and requires authentication via a bot token.

---

## Features
- Fetches the latest messages from a Discord channel.
- Adds reactions to each message.
- Uses environment variables for secure configuration.
- Implements a delay between reactions to comply with rate limits.

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/abuee422/discord-react-bot.git
cd discord-react-bot
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Configuration

### 1. Create a `.env` File
Inside the project directory, create a `.env` file and add the following:
```
AUTH_TOKEN=your_discord_bot_token
CHANNEL_ID=your_target_channel_id
EMOJI=emoji
```

### 2. Get Your Bot Token
- Go to [Discord Developer Portal](https://discord.com/developers/applications).
- Select your bot application.
- Copy the **Bot Token** and paste it into the `.env` file.

### 3. Get Your Channel ID
- Enable **Developer Mode** in Discord settings.
- Right-click on the channel where you want to add reactions and select **Copy Channel ID**.

---

## Usage
Run the bot with:
```bash
python main.py
```

The bot will:
1. Fetch the latest messages from the specified channel.
2. React to each message.
3. Display logs in the terminal.

---

## Troubleshooting

**1. Bot does not react to messages**
- Ensure the bot has **Read Messages** and **Add Reactions** permissions in the channel.
- Double-check the `AUTH_TOKEN` and `CHANNEL_ID` in `.env`.

**2. Rate Limits or API Errors**
- The bot waits **1 second between reactions** to avoid rate limits.
- If issues persist, check the API response messages for more details.

---

## License
This project is licensed under the **MIT License**.

---

## Contributing
Feel free to fork this repository and submit pull requests for improvements or new features.

