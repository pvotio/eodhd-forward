from datetime import datetime, timedelta

from client.eodhd import EODHD
from config import logger, settings


class Engine:

    TOKEN = settings.TOKEN

    def __init__(self):
        self.data = {}
        self.eodhd = EODHD(self.TOKEN)

    def run(self):
        for func in [self.fetch_ipos, self.fetch_splits, self.fetch_earnings]:
            self.data[func.__name__.split("_")[-1]] = func()

        return self.data

    def fetch_ipos(self):
        from_date = (datetime.now() - timedelta(days=365 * 5)).strftime("%Y-%m-%d")
        to_date = (datetime.now() + timedelta(days=12 * 7)).strftime("%Y-%m-%d")
        resp = self.eodhd.get_ipos(from_date=from_date, to_date=to_date)
        return resp

    def fetch_splits(self):
        from_date = (datetime.now() - timedelta(days=365 * 5)).strftime("%Y-%m-%d")
        to_date = (datetime.now() + timedelta(days=12 * 7)).strftime("%Y-%m-%d")
        resp = self.eodhd.get_splits(from_date=from_date, to_date=to_date)
        return resp

    def fetch_earnings(self):
        from_date = datetime.now()
        to_date = (from_date + timedelta(days=12 * 7)).strftime("%Y-%m-%d")
        from_date = from_date.strftime("%Y-%m-%d")
        resp = self.eodhd.get_earnings(from_date=from_date, to_date=to_date)
        return resp
