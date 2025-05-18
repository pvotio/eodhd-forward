# EODHD Forward Calendar Events Pipeline

This project implements an automated data ingestion pipeline to retrieve **forward-looking financial calendar events** such as IPOs, stock splits, and earnings announcements from the [EOD Historical Data API](https://eodhistoricaldata.com). It standardizes, transforms, and stores these datasets in a SQL Server database for use in research, investment models, and financial applications.

## Overview

### Purpose

This pipeline automates:
- Retrieval of IPO, earnings, and stock split events from the EODHD calendar API.
- Parsing and transformation of JSON responses into structured tabular data.
- Efficient loading of enriched data into SQL Server tables.

It is ideal for data platforms needing up-to-date forward-looking corporate action data.

## Source of Data

Data is pulled from the **EODHD API Calendar Endpoints**:

- `/calendar/ipos`
- `/calendar/splits`
- `/calendar/earnings`

These endpoints return JSON data of scheduled events, filtered by a custom date range (defaults to the past 5 years to ~12 weeks in the future). The pipeline requires a valid API token.

## Application Flow

The core logic is executed via `main.py` and follows this sequence:

1. **Initialize Engine**:
   - Instantiates the `Engine` object which wraps the EODHD client.

2. **Fetch Events**:
   - Invokes API methods for IPOs, splits, and earnings using predefined time windows.

3. **Transform Data**:
   - A `transformer.Agent` handles structuring, normalization, and table separation.

4. **Insert into Database**:
   - Parsed tables are inserted into SQL Server using batch inserts via `fast-to-sql`.

## Project Structure

```
eodhd-forward-main/
├── client/                # API logic and ETL engine
│   ├── engine.py          # Orchestrates fetch and routing
│   └── eodhd.py           # EODHD API wrapper for calendar endpoints
├── config/                # Logging and settings
├── database/              # MSSQL insertion logic
├── transformer/           # Transformation logic
├── main.py                # Entrypoint for execution
├── .env.sample            # Sample configuration variables
├── Dockerfile             # Docker build configuration
```

## Environment Variables

Create a `.env` file using the structure in `.env.sample`. Key variables include:

| Variable | Description |
|----------|-------------|
| `TOKEN` | EODHD API token |
| `IPOS_OUTPUT_TABLE` | SQL Server table for IPOs |
| `SPLITS_OUTPUT_TABLE` | SQL Server table for stock splits |
| `EARNINGS_OUTPUT_TABLE` | SQL Server table for earnings |
| `MSSQL_*` | Database login and connection settings |
| `REQUEST_MAX_RETRIES`, `REQUEST_BACKOFF_FACTOR` | Retry logic for API calls |
| `INSERTER_MAX_RETRIES` | Retry attempts for insertions |

## Docker Support

Run the app in a container for repeatable and portable execution.

### Build
```bash
docker build -t eodhd-forward .
```

### Run
```bash
docker run --env-file .env eodhd-forward
```

## Requirements

Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

Key libraries include:
- `requests`: API interaction
- `pandas`: Data wrangling
- `pyodbc`, `SQLAlchemy`: SQL Server support
- `fast-to-sql`: Efficient batch insertion
- `python-decouple`: Environment management

## Running the App

Ensure `.env` is populated with valid credentials and API token. Then execute:

```bash
python main.py
```

Logs will provide insights into:
- API connection success
- Number of records retrieved per category
- Insert confirmations or retry attempts

## License

This project is licensed under the MIT License. Use of the EODHD API must adhere to their published terms of service and access limits.
