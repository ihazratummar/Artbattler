
# 🏆 Discord Contest Bot

A feature-rich Discord bot for managing monthly contests in your server, from submission to voting to announcing winners — all automated using scheduled jobs.

---

## 📦 Features

- Slash command support
- Automated scheduling of contest phases:
  - Open submission
  - Close submission
  - Post to forum
  - Open voting
  - Close voting
  - Announce winner
  - Close contest
- Admin-only setup commands
- Customizable time configuration per server
- MongoDB support for persistent config and data
- DM onboarding instructions for admins

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ihazratummar/Contest-Discord-Bot.git
cd contest-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Edit `bot/config.py` to include:

- Your bot token
- MongoDB URI
- Any custom configuration

### 4. Run the Bot

```bash
python main.py
```

---

## ⚙️ First-Time Server Setup

When the bot joins a new server, it will DM the administrator with a guide:

1. `/create_contest_channel` – Create all required channels and forums
2. `/contest_role` – Assign the role allowed to submit
3. `/set_submission_open_time` – Set submission open time
4. `/set_close_submission_time` – Set submission closing time
5. `/set_post_submission_time` – Set time to post submissions to forum
6. `/set_open_voting_time` – Set time to open voting
7. `/set_close_voting_time` – Set time to close voting
8. `/set_winner_announcement_time` – Set winner announcement time
9. `/set_close_contest_time` – Set contest wrap-up time

Each command will guide the admin to the next step automatically.

---

## 📁 Project Structure

```
Contest Bot/
│
├── main.py                  # Entry point
├── requirements.txt         # Python dependencies
│
└── bot/
    ├── config.py            # Bot and DB config
    ├── core/                # Shared utilities and constants
    └── cogs/
        └── contest/
            ├── base.py      # Channel/role setup logic
            ├── commands.py  # Slash commands
            ├── jobs.py      # Scheduled job handlers
            └── utils.py     # Time validation, database updates
```

---

## 🛠 Technologies Used

- **discord.py** (with hybrid commands)
- **MongoDB** for server config
- **APScheduler** for job scheduling
- **Python 3.12+**

---

## 📬 Contributing

Pull requests are welcome. Please ensure your code is clean and follows existing patterns.

---

## 📄 License

MIT License

---

