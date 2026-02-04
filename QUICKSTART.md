# Quick Start Guide

Get your YouTube Review Agent running in **5 minutes**!

## Prerequisites

- Python 3.11+
- [LM Studio](https://lmstudio.ai/) installed
- Telegram account
- YouTube Data API v3 Key

## Setup Steps

### 1. Install Dependencies (1 min)
```bash
pip install -r requirements.txt
```

### 2. Start LM Studio (2 min)
1. Open LM Studio
2. Load a model (e.g., Mistral 7B, Llama, etc.)
3. Go to "Local Server" tab
4. Click "Start Server"
5. **Note the model name** shown in the server tab

### 3. Create Telegram Bot (1 min)
1. Open Telegram, search for `@BotFather`
2. Send: `/newbot`
3. Choose a name and username
4. **Copy the bot token** (looks like `123456789:ABC...`)
5. Send any message to your new bot

### 4. Get YouTube API Key (2 min)
1. Go to the [Google Cloud Console](https://console.cloud.google.com/apis/library/youtube.googleapis.com).
2. Create a new project (or select an existing one).
3. Enable the "YouTube Data API v3".
4. Go to "Credentials", click "Create Credentials", and choose "API key".
5. **Copy the API key**.

### 5. Get Your Chat ID (30 sec)
```bash
python get_chat_id.py
```
Enter your bot token when prompted, then **copy your chat ID**.

### 6. Configure (1 min)

**Create `.env` file:**
```bash
# Windows
copy .env.example .env

# Linux/macOS
cp .env.example .env
```

**Edit `.env`** and add your tokens:
```
TELEGRAM_BOT_TOKEN="your_actual_token_here"
YOUTUBE_API_KEY="your_api_key_here"
```

**Create `config.yaml`:**
```bash
# Windows
copy config.example.yaml config.yaml

# Linux/macOS
cp config.example.yaml config.yaml
```

**Edit `config.yaml`:**
```yaml
channels:
  - name: "Fireship"
    identifier: "@Fireship" # Use channel handle, ID (UC...), or URL
  - name: "ThePrimeagen"
    identifier: "@ThePrimeagen"

telegram:
  chat_id: 123456789  # Your chat ID from step 5

llm:
  model: "zai-org/glm-4.7-flash"  # Your model name from LM Studio
```

### 7. Run! (30 sec)

**Option A: One-time run**
```bash
python -m yt_agent.cli --config config.yaml
```

**Option B: Interactive bot mode** 📱
```bash
# Windows
run_bot.bat

# Linux/macOS
./run_bot.sh

# Or manually
python -m yt_agent.cli --config config.yaml --bot
```

Then send `/review` to your bot on Telegram!

## 🎉 Success!

You should receive a Telegram message with video summaries!

## Bot Commands (Interactive Mode)

When running in bot mode (`--bot` flag):

- `/review` - Get video summaries on demand
- `/status` - Check agent status
- `/clean` - Delete chat history (last 48h)
- `/help` - Show available commands

## Troubleshooting

**"Python was not found"**
- Install Python 3.11+ from python.org
- Or use `python3` instead of `python`

**"TELEGRAM_BOT_TOKEN environment variable is required"**
- Make sure you created `.env` file
- Check the token is correct (no quotes, no spaces)

**"LLM request failed"**
- Ensure LM Studio server is running (green indicator)
- Check the model name matches exactly

**"No transcript found"**
- Normal! Not all videos have transcripts
- The agent will use the description instead

**"Failed to send Telegram message"**
- Double-check your bot token in `.env`
- Make sure you sent a message to the bot first
- Verify the chat ID is correct in `config.yaml`

**Bot doesn't respond to commands**
- Check the agent is running in bot mode (`--bot` flag)
- Verify chat ID matches yours
- Look at terminal output for errors

## Next Steps

### Schedule Daily Reports
Set up automatic daily reviews:

**Windows Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at 9 AM)
4. Action: `python -m yt_agent.cli --config C:\path\to\config.yaml`

**Linux/macOS Cron:**
```bash
crontab -e
# Add: 0 9 * * * cd /path/to/YouTube_Bot && python -m yt_agent.cli --config config.yaml
```

### Run Bot 24/7
Keep the agent running to trigger reviews anytime from your phone:

**Windows:**
```cmd
start /B run_bot.bat
```

**Linux/macOS:**
```bash
nohup ./run_bot.sh > bot.log 2>&1 &
```

### Customize
Edit `config.yaml`:
- `max_videos_per_channel`: 1-5 (how many videos to check)
- `max_sentences_per_video`: 3-10 (summary length)
- `temperature`: 0.1-0.5 (more focused/creative)
- `language`: "en", "de", "fr", etc.

### Add More Channels
Just add more entries to the `channels` list in `config.yaml`!

## Full Documentation

- 📖 [README.md](README.md) - Complete documentation
- 🔒 [SECURITY.md](SECURITY.md) - Security best practices
- 📋 [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup instructions

---

**Need help?** Run with `--verbose` flag for detailed logs:
```bash
python -m yt_agent.cli --config config.yaml --verbose
```
