# MCX Gold Futures Tracker & Dashboard 📈

A lightweight, automated tracking system and web dashboard designed to fetch, log, and visualize live MCX (Multi Commodity Exchange) Gold futures data. 

The repository uses Python scripts to retrieve market data, structure payload logs into JSON, and auto-commit updates using GitHub Actions to present real-time metrics on a simple frontend dashboard.

---

## 🚀 Key Features

* **Automated Data Fetching:** Python-based scrapers/API integration to pull latest commodity pricing and contract details.
* **Structured Storage:** Converts dynamic market feeds into structured `JSON` payloads for seamless parsing.
* **GitHub Actions Automation:** Scheduled workflow executions that regularly commit updated data snapshots directly to the repository.
* **Interactive Dashboard:** Clean, responsive web UI (HTML/CSS/JS) to monitor real-time trends and historical price shifts.

---

## 🛠 Tech Stack

* **Language:** Python 3.x
* **Frontend:** HTML5, CSS3, JavaScript
* **Data Format:** JSON
* **Automation & CI/CD:** GitHub Actions
* **Version Control:** Git & GitHub

---

## 📂 Project Structure

```text
mcx/
├── .github/
│   └── workflows/
│       └── update-data.yml    # Automated scheduled run for updater script
├── data/
│   └── mcx_data.json          # Formatted dataset/payload
├── scripts/
│   └── fetch_mcx.py           # Core logic for fetching & updating data
├── index.html                 # Main dashboard interface
├── style.css                  # UI styling
├── script.js                  # Frontend data parsing & chart loading
└── README.md                  # Project documentation
