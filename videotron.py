import requests
import json
import datetime


class Videotron:
    def __init__(self, config):
        self.config = config

    def get_current_month_usage(self):
        session = requests.session()

        usage = json.loads(session.get("https://www.videotron.com/api/1.0/internet/usage/wired/"+self.config["userkey"]+".json?lang=en&caller=videotron-mac.pommepause.com").content)

        update_date = datetime.datetime.strptime(usage["internetAccounts"][0]["usageTimestamp"], '%Y-%m-%dT%H:%M%z').strftime('%Y-%m-%d %H:%M')
        current_monthly_usage = "{0:.3}".format((usage["internetAccounts"][0]["downloadedBytes"] + usage["internetAccounts"][0]["uploadedBytes"]) / (1024 * 1024 * 1024))
        maximum_monthly_usage = (usage["internetAccounts"][0]["maxCombinedBytes"]) / (1024 * 1024 * 1024)
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