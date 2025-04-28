# 🚀 Crypto MMS API

A **FastAPI** service for calculating and serving moving averages (MMS) of cryptocurrency prices.

---

## 📋 Table of Contents
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the API](#running-the-api)
- [Data Population Scripts](#data-population-scripts)
- [Development](#development)
- [API Documentation](#api-documentation)
- [Notes](#notes)

---

## 🛠️ Getting Started

### Prerequisites
- **Python**: Version 3.12 or higher
- **Docker**: For running the local database
- **UV**: Recommended for dependency management

---

## 📦 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/javiersrf/mb-challenger.git
   cd mb-challenger
   ```

2. **Set Up dependencies**:
   [Install uv dependency manager](https://docs.astral.sh/uv/getting-started/installation/)
   or
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file from the sample:
   ```bash
   cp .env.sample .env
   ```
   Update the `.env` file with your configuration.

4. **Install Dependencies**:
   Using Poetry:
   ```bash
   uv sync
   ```

---

## 🗄️ Database Setup

Start the database using Docker Compose:
```bash
docker compose up -d
```

---

## ▶️ Running the API

Start the FastAPI server:
```bash
make run
```

The API will be available at: [http://localhost:8000](http://localhost:8000)

---

## 📊 Data Population Scripts

### Populate with 1 Year of Historical Data
Calculate and store MMS values using 1 year of historical data up to today:
```bash
uvicorn run -m scripts.populate_initial
```

### Populate with a Custom Date Range
Calculate MMS for a specific date range (using Unix timestamps):
```bash
uvicorn run scripts.populate_table_by_range --from 1672531200 --to 1680288000
```

Example timestamps:
- `1672531200` = Jan 1, 2023
- `1680288000` = Mar 31, 2023

### Update Today's Values
Calculate and store only today's MMS values:
```bash
uvicorn run scripts.populate_today
```

---

## 🛠️ Development

### Running Tests
Run the test suite:
```bash
make test
```

### Linting and Formatting
- **Linting**:
  ```bash
  make lint
  ```
- **Auto-formatting**:
  ```bash
  make format
  ```

---

## 📖 API Documentation

After starting the server, you can access the API documentation:

- **Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative Docs**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📝 Notes

- The database will be automatically migrated on the first run.
- All population scripts will only store complete MMS values (20, 50, and 200-day).
- Historical data is required for accurate moving average calculations.

---
