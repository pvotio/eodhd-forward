# EODHD Forward
## Overview
EODHD Forward is a Python-based data pipeline that interacts with the EOD Historical Data API to fetch financial data related to IPOs, stock splits, and earnings reports. The retrieved data is processed and stored in a Microsoft SQL Server database.

## Features
- Fetches IPO, stock split, and earnings data from EODHD API.
- Uses retry mechanisms for robust API communication.
- Transforms raw data into structured formats.
- Stores data into a Microsoft SQL Server database.
- Dockerized for easy deployment.

## Installation
### Prerequisites
- Python 3.10+
- Microsoft SQL Server
- Docker (optional, for containerized execution)

### Setup
Clone the repository:

```bash
git clone https://github.com/arqs-io/eodhd-forward.git
cd eodhd-forward
```

Install dependencies:

`pip install -r requirements.txt`

Set up environment variables:

- Copy .env.sample to .env
- Edit .env to include your database and API credentials.

Run the application:
`python main.py`

## Docker Usage

To run the application using Docker:


```bash
docker build -t eodhd-forward .
docker run --env-file .env eodhd-forward
```

## Contributing
- Fork the repository.
- Create a feature branch: git checkout -b feature-branch
- Commit changes: git commit -m "Add new feature"
- Push to the branch: git push origin feature-branch
- Open a Pull Request.