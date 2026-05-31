# 🔐 Windows Keylogger

> A lightweight, stealth keylogger for Windows with Telegram-based exfiltration.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows-green.svg?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-red.svg?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Telegram-Bot-orange.svg?style=for-the-badge" alt="Telegram">
  <img src="https://img.shields.io/github/stars/stein-exe/keylogger?style=for-the-badge" alt="Stars" link="https://github.com/stein-exe/keylogger">
  <img src="https://img.shields.io/visitor?label=Visitors&style=for-the-badge&color=blue" alt="Visitors">
</p>

---

## ⚡ Features

| Feature | Description |
|---|---|
| 🔍 **Real-time Logging** | Captures every keystroke with active window tracking |
| 📱 **Telegram Alerts** | Sends logs directly to your Telegram bot |
| 🧅 **Self Persistence** | Survives reboots, re-copies itself to AppData |
| 💻 **Stealth Mode** | Runs hidden with no console window |
| 🚀 **Auto Startup** | Registers itself in Windows Startup |
| 📦 **Single File** | Zero dependencies — auto-installs packages |

---

## ⚙️ Configuration

Edit the config section in `loger.py`:

```python
# ================= CONFIG =================
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"
SEND_INTERVAL = 20
MAX_MSG_LEN = 4000
# =========================================
```

### Getting your Telegram credentials:

1. **Bot Token** — Message [@BotFather](https://t.me/BotFather) on Telegram
2. **Chat ID** — Message [@userinfobot](https://t.me/userinfobot) to get your ID

---

## 📁 Project Structure

```
keylogger/
├── loger.py      # Main executable
└── README.md     # This file
```

---

## 🔒 Security Notes

- Logs are sent **every 20 seconds** (configurable)
- All transmission is over **HTTPS**
- Logs include: timestamp, PC name, username, active window, keystrokes
- Data is stored only in your Telegram chat

---

## ⚠️ Disclaimer

> This tool is intended for **educational purposes** and **authorized security testing only**. Unauthorized keylogging is **illegal** and **unethical**. The author is not responsible for misuse.

---

## 📜 Credits

<div align="center">

**Developed by [Stein](https://t.me/rejerk)** — reach out anytime.

Questions? Join the discussion: **[Telegram Group](https://t.me/keped)**

</div>

---

<p align="center">
  ⭐ If this project helped you — star it!
</p>
