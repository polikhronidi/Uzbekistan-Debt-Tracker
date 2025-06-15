# Uzbekistan Debt Tracker Bot

**A comprehensive, multilingual Telegram bot for real-time monitoring, visualization, and deep analysis of Uzbekistan’s national debt.**

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Motivation & Background](#motivation--background)  
3. [Key Features](#key-features)  
4. [Architecture & Design](#architecture--design)  
   - [Module Structure](#module-structure)  
   - [Database Schema](#database-schema)  
   - [Utility Functions](#utility-functions)  
   - [Localization Layer](#localization-layer)  
5. [Installation & Setup](#installation--setup)  
   - [Prerequisites](#prerequisites)  
   - [Environment Setup](#environment-setup)  
   - [Cloning the Repository](#cloning-the-repository)  
   - [Virtual Environment & Dependencies](#virtual-environment--dependencies)  
   - [Configuration & Environment Variables](#configuration--environment-variables)  
6. [Running the Bot Locally](#running-the-bot-locally)  
7. [Bot Commands & Usage](#bot-commands--usage)  
8. [Deployment](#deployment)  
   - [Docker Compose Setup](#docker-compose-setup)  
   - [CI/CD Integration](#cicd-integration)  
   - [Monitoring & Logging](#monitoring--logging)  
9. [Performance & Scalability](#performance--scalability)  
10. [Security Considerations](#security-considerations)  
11. [Testing](#testing)  
12. [Troubleshooting & FAQ](#troubleshooting--faq)  
13. [Roadmap & Future Enhancements](#roadmap--future-enhancements)  
14. [Contribution Guidelines](#contribution-guidelines)  
15. [License](#license)  
16. [Acknowledgements](#acknowledgements)  
17. [Contact Information](#contact-information)  
---

## Project Overview

The Uzbekistan Debt Tracker Bot is a Telegram-based analytics tool that fetches, processes, and visualizes data on the national debt of Uzbekistan in real time. Leveraging the World Bank’s public API, the bot provides interactive charts, historical trends, per-capita calculations, regional breakdowns, and multilingual support (Russian, English, Uzbek). It’s designed for economists, government analysts, journalists, investors, and curious citizens who want transparent, up-to-date insights into the country’s financial obligations.

---

## Motivation & Background

With the ever-increasing importance of data transparency and open government, tracking national debt publicly is paramount. Traditional web dashboards can be cumbersome or gated behind paywalls. By integrating debt analytics directly into Telegram—a platform with over 500 million active users—this bot:
- **Democratizes financial data**: Anyone with Telegram can access key debt metrics.  
- **Encourages civic engagement**: Citizens stay informed and can discuss policy.  
- **Streamlines analysis**: Instant charts, historical comparisons, and notifications.  
- **Enables automation**: Scheduled updates and webhook alerts keep stakeholders alerted.  

---

## Key Features

- **Real-time Data Fetching**  
- **Historical Growth Charts**  
- **Animation of Debt Dynamics**  
- **Per-Capita Calculations**  
- **Regional Debt Rankings**  
- **Multilingual Support**  
- **Rate Limiting & Throttling**  
- **Automated Broadcasts**  
- **Configurable Settings**  
- **Extensible Architecture**

---

## Architecture & Design

Modular structure with separate folders for commands, handlers, keyboards, middleware, utilities, and localization. SQLite used for user data; World Bank API for debt figures; Matplotlib for charts and GIFs; aiogram for Telegram integration.

---

## Installation & Setup

```bash
git clone https://github.com/polikhronidi/Uzbekistan-Debt-Tracker.git
cd Uzbekistan-Debt-Tracker
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

Create a `.env` file:
```ini
TOKEN=<YOUR_BOT_TOKEN>
API_URL=http://api.worldbank.org/v2/country/uz/indicator/DT.DOD.DECT.CD?format=json&per_page=100
MINUTE_LIMIT=60
HOUR_LIMIT=150
```

---

## Running the Bot Locally

```bash
python main.py
```

---

## Bot Commands & Usage

| Command    | Description                                        |
| ---------- | -------------------------------------------------- |
| `/start`   | Initialize and choose language                     |
| `/history` | Show historical debt chart and animation button    |
| `/mydebt`  | Display per-capita debt                            |
| `/faq`     | Explain what national debt is                      |
| `/regions` | List regions and show ranking                      |
| `/help`    | Show available commands                            |

---

## Deployment

- **Docker Compose**  
- **CI/CD** with GitHub Actions  
- **Monitoring** via logs and health checks  

---

## Performance & Scalability

- Async I/O  
- Rate limiting  
- Caching possibilities  
- Horizontal scaling  

---

## Security Considerations

- Token protection (use `.env`)  
- Database encryption or external DB  
- Dependency audits  
- Input validation  

---

## Testing

- Unit tests with pytest  
- Mocks for API calls  
- Linting/formatting via flake8, black  

---

## Troubleshooting & FAQ

- Missing glyph warnings → install emoji fonts  
- Slow GIF generation → reduce frames or cache  
- Database locked → use check_same_thread=False or external DB  

---

## Roadmap & Future Enhancements

- Debt-to-GDP ratio  
- Threshold-based alerts  
- Multi-country support  
- GraphQL API  

---

## Contribution Guidelines

Thank you for your interest!  
1. Fork the repo  
2. Create a branch: `feature/your-feature`  
3. Implement changes and tests  
4. Lint and format your code  
5. Push and open a PR

---

## License

MIT License. See [LICENSE](LICENSE).

---

## Acknowledgements

- World Bank Open Data  
- aiogram, aiohttp, matplotlib, numpy communities  

---

## Contact Information

**Author:** Oleg Polikhronidi  
**GitHub:** https://github.com/polikhronidi  
**Email:** pn198047foleg33@gmail.com
