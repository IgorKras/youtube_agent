<div align="center">

# 📺 YouTube Review Agent

**AI-powered YouTube summaries delivered to your Telegram — 100% local, no cloud AI required**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![LM Studio](https://img.shields.io/badge/LLM-LM%20Studio-purple.svg)](https://lmstudio.ai/)

[Quick Start](#-quick-start) •
[Features](#-features) •
[How It Works](#-how-it-works) •
[Configuration](#%EF%B8%8F-configuration) •
[Documentation](#-documentation)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI Agent** | Natural language understanding — just say "Add channel @Fireship" |
| 🔒 **100% Local** | Runs on your machine with LM Studio — no API or cloud costs |
| 📱 **Telegram Bot** | Get summaries on your phone, trigger reviews anytime |
| 📝 **Smart Summaries** | Uses video transcripts, falls back to description when unavailable |
| ⚙️ **Flexible** | Run on-demand, as a bot, or scheduled via cron/Task Scheduler |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** — [Download](https://www.python.org/downloads/)
- **LM Studio** — [Download](https://lmstudio.ai/) (free, runs local LLMs)
- **Telegram account** — For the bot
- **YouTube API key** — Free tier is sufficient

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/YouTube_Bot.git
cd YouTube_Bot
pip install -r requirements.txt
```

### 2. Set Up LM Studio

1. Open LM Studio and download a model (e.g., `Mistral 7B`, `Llama 3`, or `GLM-4`)
2. Go to **Local Server** tab → Click **Start Server**
3. Note the **model name** shown in the server tab

### 3. Create Telegram Bot

1. Open Telegram, search for **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy your **bot token** (format: `123456789:ABC-DEF...`)
4. **Important:** Send any message to your new bot to activate it

### 4. Get YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/library/youtube.googleapis.com)
2. Create a project → Enable **YouTube Data API v3**
3. Go to **Credentials** → **Create Credentials** → **API Key**
4. Copy the API key

### 5. Configure

```bash
# Copy example files
cp .env.example .env
cp config.example.yaml config.yaml

# Get your Telegram chat ID
python get_chat_id.py
```

Edit `.env`:
```env
TELEGRAM_BOT_TOKEN="your_bot_token_here"
YOUTUBE_API_KEY="your_api_key_here"
```

Edit `config.yaml`:
```yaml
telegram:
  chat_id: 0123456789  # Your chat ID from get_chat_id.py

llm:
  model: "your-model-name"  # From LM Studio
```

### 6. Run!

```bash
# Interactive bot mode (recommended)
python -m yt_agent.cli --config config.yaml --bot

# Or use the convenience script
# Windows: run_bot.bat
# Linux/macOS: ./run_bot.sh
```

Then open Telegram and send `/review` to your bot! 🎉

---

## 🎯 How It Works

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   You on        │────▶│   YouTube Bot    │────▶│   LM Studio     │
│   Telegram      │     │   (Python)       │     │   (Local LLM)   │
└─────────────────┘     └────────┬─────────┘     └─────────────────┘
                                 │
                        ┌────────▼─────────┐
                        │   YouTube API    │
                        │   (Transcripts)  │
                        └──────────────────┘
```

1. **You send a command** via Telegram (e.g., "Run review" or `/review`)
2. **The agent fetches** latest videos from your monitored channels
3. **Transcripts are retrieved** via YouTube's API
4. **Your local LLM** generates concise summaries
5. **Results are sent** back to your Telegram chat

---

## 💬 Bot Commands

### Slash Commands
| Command | Description |
|---------|-------------|
| `/review` | Run a review of all channels |
| `/status` | Check agent status |
| `/clean` | Clear chat history |
| `/help` | Show available commands |

### Natural Language
The agent understands plain English:
- *"Add channel @Fireship"*
- *"Remove channel ThePrimeagen"*
- *"List my channels"*
- *"What's new on my channels?"*

---

## ⚙️ Configuration

### config.yaml

```yaml
run:
  timezone: "Europe/Vienna"       # Your timezone
  max_videos_per_channel: 1       # Videos to check per channel (1-5)

telegram:
  chat_id: 123456789              # Your Telegram chat ID

llm:
  api_base: "http://127.0.0.1:1234"  # LM Studio endpoint
  model: "zai-org/glm-4.7-flash"     # Model name from LM Studio
  temperature: 0.2                    # Lower = more focused
  max_sentences_per_video: 3          # Summary length
  language: "en"                      # Output language
  include_links: true                 # Include video links
  group_by_channel: true              # Group videos by channel
  title: "YouTube Daily Review"       # Report title
```

### Managing Channels

Channels are stored in `channels.json` (gitignored for privacy) and can be managed via bot commands:

```
"Add channel @Fireship"
"Remove channel Lex Fridman"
"List channels"
```

**First-time setup:** Copy the example file:
```bash
cp channels.example.json channels.json
```

Or the bot will create `channels.json` automatically when you add your first channel.

---

## 📅 Scheduling

### Run Daily Reviews Automatically

**Windows Task Scheduler:**
```
Program: python
Arguments: -m yt_agent.cli --config C:\path\to\config.yaml
Start in: C:\path\to\YouTube_Bot
```

**Linux/macOS (cron):**
```bash
# Run daily at 9 AM
0 9 * * * cd /path/to/YouTube_Bot && python -m yt_agent.cli --config config.yaml
```

### Run Bot 24/7

**Linux/macOS:**
```bash
nohup ./run_bot.sh > bot.log 2>&1 &
```

**Windows:**
```cmd
start /B run_bot.bat
```

---

## 🔧 Troubleshooting

<details>
<summary><b>LLM request failed</b></summary>

- Ensure LM Studio server is running (green indicator)
- Verify the model name in `config.yaml` matches exactly what LM Studio shows
- Check `http://127.0.0.1:1234/v1/models` returns a response
</details>

<details>
<summary><b>Telegram bot doesn't respond</b></summary>

- Make sure you're running with `--bot` flag
- Verify `chat_id` in `config.yaml` matches yours
- Check that you sent a message to the bot first
- Look at terminal output for error messages
</details>

<details>
<summary><b>No transcript found</b></summary>

- This is normal — not all videos have transcripts
- The agent automatically falls back to using the video description
</details>

<details>
<summary><b>YouTube API errors</b></summary>

- Verify your API key is correct in `.env`
- Check your API quota at [Google Cloud Console](https://console.cloud.google.com/apis/dashboard)
- The free tier allows ~10,000 requests/day
</details>

---

## 📁 Project Structure

```
YouTube_Bot/
├── yt_agent/              # Core agent code
│   ├── review_agent.py    # Main agent logic
│   ├── langchain_utils.py # LLM integration
│   ├── youtube_client.py  # YouTube API client
│   ├── telegram_client.py # Telegram bot client
│   └── ...
├── config.yaml            # Your configuration
├── channels.json          # Monitored channels
├── .env                   # API keys (not committed)
├── run_bot.bat/.sh        # Convenience scripts
└── README.md
```

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | Step-by-step setup guide |
| [SECURITY.md](SECURITY.md) | Security best practices |

---

## 🔒 Security

- **Never commit** your `.env` file — it contains API keys
- Store sensitive tokens **only** in `.env`
- The bot only responds to your configured `chat_id`
- See [SECURITY.md](SECURITY.md) for details

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**[⬆ Back to Top](#-youtube-review-agent)**

Made with ❤️ for YouTube/AI enthusiasts who value their privacy

</div>
