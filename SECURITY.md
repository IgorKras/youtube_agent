# Security Best Practices for YouTube Telegram Review Agent

## ✅ What We've Implemented

This project now follows security best practices for managing sensitive credentials:

### 1. Environment Variables via `.env` File
- **All sensitive tokens** (Telegram bot token, API keys) are stored in a `.env` file
- The `.env` file is **automatically loaded** by `python-dotenv` 
- The `.env` file is **gitignored** to prevent accidental commits

### 2. No Hardcoded Secrets
- ❌ Tokens are **never** hardcoded in source code
- ❌ Tokens are **never** committed to version control
- ❌ Tokens are **never** shared in documentation

### 3. Template File
- `.env.example` provides a template without real credentials
- Users copy `.env.example` to `.env` and add their own tokens

---

## 🔐 How to Set Up Your Credentials

### Step 1: Create Your `.env` File

**Windows (PowerShell):**
```powershell
copy .env.example .env
```

**Linux/macOS:**
```bash
cp .env.example .env
```

### Step 2: Edit the `.env` File

Open `.env` in any text editor and add your credentials:

```
TELEGRAM_BOT_TOKEN=your_actual_token_here
```

**To get your Telegram bot token:**
1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the instructions
3. Copy the token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
4. Paste it in your `.env` file

### Step 3: Verify Setup

Run the verification script:
```powershell
python verify_setup.py
```

---

## ⚠️ IMPORTANT Security Rules

### DO ✅
- ✅ Keep your `.env` file **local only** (never commit it)
- ✅ Use `.env.example` as a template for others
- ✅ Regenerate tokens if they are ever exposed
- ✅ Use different tokens for development and production

### DON'T ❌
- ❌ **Never** commit `.env` to git
- ❌ **Never** share your `.env` file
- ❌ **Never** post tokens in issues, forums, or chat
- ❌ **Never** hardcode tokens in scripts or code
- ❌ **Never** include tokens in screenshots

---

## 🔄 What Changed (Migration from Old Setup)

If you were using the old setup with hardcoded tokens:

### Old Way (INSECURE ❌)
```powershell
# In run.bat or PowerShell
set TELEGRAM_BOT_TOKEN=your_actual_token_here
python -m yt_agent.cli --config config.yaml
```

### New Way (SECURE ✅)
```powershell
# Create .env file once:
copy .env.example .env
# Edit .env and add your token

# Then just run:
python -m yt_agent.cli --config config.yaml
```

The token is automatically loaded from `.env` by `python-dotenv`.

---

## 🛡️ What If My Token Was Exposed?

If you accidentally committed or shared your token:

1. **Revoke the old token immediately:**
   - Go to [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/mybots`
   - Select your bot
   - Click "API Token" → "Revoke current token"

2. **Generate a new token:**
   - In BotFather, click "Generate new token"
   - Update your `.env` file with the new token

3. **Clean git history** (if committed):
   ```bash
   # Remove from git history (advanced)
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```

---

## 📚 Additional Resources

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [Telegram Bot Security Best Practices](https://core.telegram.org/bots/faq#security)

---

## 🔍 Verification Checklist

Before sharing your code or pushing to a repository:

- [ ] `.env` file is in `.gitignore`
- [ ] No tokens in source code files
- [ ] No tokens in documentation files
- [ ] No tokens in batch/shell scripts
- [ ] `.env.example` has placeholder values only
- [ ] Run `git status` to verify `.env` is not tracked

---

**Remember:** Treat your bot token like a password. If it's exposed, anyone can control your bot!
