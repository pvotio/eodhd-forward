from urllib.parse import urljoin

import requests

from client.request import init_session
from config import logger, settings


class EODHD:

    BASE = "https://eodhistoricaldata.com/api/"

    def __init__(self, token):
        self.token = token
        self.session = init_session(
            settings.REQUEST_MAX_RETRIES, settings.REQUEST_BACKOFF_FACTOR
        )

    def request(self, method, *args, **kwargs):
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
        }
        kwargs["headers"] = headers
        if not "params" in kwargs:
            kwargs["params"] = {}

        kwargs["params"].update(self.params)
        logger.debug(f"Request headers: {headers}")
        logger.debug(f"Request parameters: {kwargs['params']}")

        try:
            response = self.session.request(method, *args, **kwargs)
            if response.status_code == 404:
                raise ValueError("Symbol not found on EODHD API")

            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {args[0]}: {str(e)}")
            raise

    def get_ipos(self, from_date, to_date):
        url = urljoin(self.BASE, f"calendar/ipos")
        params = {"from": from_date, "to": to_date}
        resp = self.request("get", url, params=params)
        return resp.json()

    def get_splits(self, from_date, to_date):
        url = urljoin(self.BASE, f"calendar/splits")
        params = {"from": from_date, "to": to_date}
        resp = self.request("get", url, params=params)
        return resp.json()

    def get_earnings(self, from_date, to_date):
        url = urljoin(self.BASE, f"calendar/earnings")
        params = {"from": from_date, "to": to_date}
        resp = self.request("get", url, params=params)
        return resp.json()

    @property
    def params(self):
        logger.debug("Generating request parameters with API token.")
        return {"api_token": self.token, "fmt": "json"}
