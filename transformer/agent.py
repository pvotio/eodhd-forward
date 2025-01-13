from datetime import datetime

import pandas as pd

from config import settings


class Agent:
    def __init__(self, data):
        self.data = data

    def transform(self):
        result = {
            "ipos": [settings.IPOS_OUTPUT_TABLE, []],
            "splits": [settings.SPLITS_OUTPUT_TABLE, []],
            "earnings": [settings.EARNINGS_OUTPUT_TABLE, []],
        }

        fields = {
            "ipos": [
                "name",
                "exchange",
                "currency",
                "start_date",
                "filing_date",
                "amended_date",
                "price_from",
                "price_to",
                "offer_price",
                "shares",
                "deal_type",
            ],
            "splits": ["split_date", "optionable", "old_shares", "new_shares"],
            "earnings": [
                "report_date",
                "date",
                "before_after_market",
                "currency",
                "actual",
                "estimate",
                "difference",
                "percent",
            ],
        }

        for k in result:
            if k in self.data:
                for i in self.data[k][k]:

                    _result = {"eodhd_ticker": i["code"]}

                    for key in fields[k]:

                        if "#" in key:
                            key, name = key.split("#")
                        else:
                            name = key

                        if key in i:
                            if "date" in key.lower():
                                _result[name] = self.valcheck_date(i[key])
                            else:
                                _result[name] = self.valcheck(i[key])
                        else:
                            _result[name] = None

                    _result["timestamp_created_utc"] = self.timenow()
                    result[k][1].append(_result)

        return {data[0]: pd.DataFrame(data[1]) for _, data in result.items()}

    @staticmethod
    def valcheck(value):
        if value in ["NA", "NaN", "", 0, "0", None]:
            return None

        elif isinstance(value, int):
            return round(float(value), 4)

        else:
            return value

    @staticmethod
    def valcheck_date(value):
        if value in ["NA", "NaN", "", 0, "0", None]:
            return None

        if "T" in value:
            value = value.split("T")[0]
        try:
            x = datetime.strptime(value, "%Y-%m-%d")
            if x.year < 1900:
                return None

            return value
        except Exception:
            return None

    @staticmethod
    def timenow():
        return datetime.utcnow()
