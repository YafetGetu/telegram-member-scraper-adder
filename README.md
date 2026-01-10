# Telegram Member Scraper and Adder

A Python tool for managing Telegram group members using the Telethon API.  
For educational purposes only.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Telethon](https://img.shields.io/badge/Telethon-1.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Educational](https://img.shields.io/badge/For-Educational%20Use-red.svg)
![Platform](https://img.shields.io/badge/Platform-Telegram-0088cc.svg)

---

## Star This Repository

If you find this project useful for learning about Telegram APIs, please give it a star to show your support.

---

## IMPORTANT DISCLAIMER

THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY.

- Do NOT use this for spamming or harassment  
- Only use with groups you administrate  
- Only add users who explicitly consent  
- Respect Telegram's Terms of Service  
- Violating Telegram ToS can result in account bans  
- This code is for learning purposes only  

---

## Prerequisites

1. Python 3.7 or higher  
2. Active Telegram account  
3. Telegram API credentials (https://my.telegram.org)  
4. Admin rights in target groups (for adding members)  

---

## Installation

### Clone the repository

```bash
git clone https://github.com/YafetGetu/tg-member-scraper.git
cd tg-member-scraper
````

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Telegram API Setup

1. Visit [https://my.telegram.org](https://my.telegram.org)
2. Login with your Telegram account
3. Go to **API Development Tools**
4. Create a new application
5. Copy your `api_id` and `api_hash`

---

## Environment Variables

Create a `.env` file and add your credentials:

```env
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
```

---

## Project Structure

```
tg-member-scraper/
├── csv/                    # CSV files storage
├── mem_scrap.py            # Member scraping tool
├── add_mem.py              # Member adding tool
├── requirements.txt        # Python dependencies
├── .env_example            # Environment template
├── .gitignore              # Git ignore file
└── README.md               # Documentation
```

---

## Tools

### Member Scraper (`mem_scrap.py`)

Scrapes member data from a Telegram group and saves it to CSV.

**Features:**

* Collects usernames and user IDs
* Saves output to CSV
* Uses Telethon async API

**Usage:**

```bash
python mem_scrap.py
```

---

### Member Adder (`add_mem.py`)

Adds members to a Telegram group from a CSV file.

**Features:**

* Reads users from CSV
* Includes delay to reduce flood risk
* Handles common Telethon errors
* Prints progress and errors

**Usage:**

```bash
python add_mem.py
```

---

## CSV Format

Both tools use CSV files in this format:

```csv
username,id
username1,123456789
username2,987654321
```

CSV files are automatically saved to and loaded from the `csv/` directory.

---

## Security and Privacy

Before using this tool:

* Never commit `.env` or session files
* Use a secondary Telegram account if possible
* Do not reduce delay values
* Keep API credentials private
* Follow Telegram Terms of Service

Recommended `.gitignore` entries:

```
.env
*.session
```

---

## Responsible Usage

### DO

* Use this tool for learning API integration
* Test on private or owned groups
* Ask permission before adding users
* Respect user privacy

### DO NOT

* Spam users
* Add members without consent
* Bypass Telegram restrictions
* Use for commercial or malicious purposes

---

## Troubleshooting

### FloodWait errors

* Wait the specified number of seconds
* Do not lower delay times

### Cannot access group

* Ensure you are a member
* Verify group exists
* Confirm admin permissions

### API errors

* Verify API credentials
* Check internet connection
* Ensure Telegram account is active

### Session files not found

* Run the tool once to create session files
* Make sure you have write permissions

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Final Notice

This tool is intended for educational purposes only.
The author assumes no responsibility for misuse or violations of Telegram’s Terms of Service.

If this project helped you learn something new, consider starring the repository.

