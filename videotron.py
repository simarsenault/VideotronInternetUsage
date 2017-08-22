import requests
import json
from dateutil import parser


class Videotron:
    def __init__(self, config):
        self.config = config

    def get_current_month_usage(self):
        session = requests.session()

        usage = json.loads(session.get("https://www.videotron.com/api/1.0/internet/usage/wired/"+self.config["userkey"]+".json?lang=en&caller=videotron-mac.pommepause.com").content)

        update_date = parser.parse(usage["internetAccounts"][0]["usageTimestamp"]).strftime('%Y-%m-%d %H:%M')
        current_monthly_usage = "{0:.5g}".format(self._convert_bytes_to_gigabytes(usage["internetAccounts"][0]["downloadedBytes"] + usage["internetAccounts"][0]["uploadedBytes"]))
        maximum_monthly_usage = self._convert_bytes_to_gigabytes(usage["internetAccounts"][0]["maxCombinedBytes"])
        unit = 'GB'
        days_remaining = usage["daysToEnd"]

        session.close()

        return {
            'update_date': update_date,
            'usage': current_monthly_usage,
            'maximum': maximum_monthly_usage,
            'unit': unit,
            'days_remaining': days_remaining
        }

    def _convert_bytes_to_gigabytes(self, _bytes):
        return _bytes / 1073741824
