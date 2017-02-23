import requests
import re


class Videotron:
    PATTERN_INPUT_HIDDEN = re.compile(r"<input type=\"hidden\" name=\"(?P<tokenName>\w+)\" value=\"(?P<tokenValue>[\w.]+)\">")
    PATTERN_MONTHLY_INTERNET_USAGE = re.compile(r"<span class=\"quantities\">(?P<current>[\d.]+) / (?P<maximum>[\d.]+).*</span>")
    PATTERN_DAYS_IN_MONTH_REMAINING = re.compile(r"<p class=\"note_reset\">Number of days before reverting to zero: (?P<daysLeft>\d+) days?</p>")

    def __init__(self, config):
        self.config = config

    def get_current_month_usage(self):
        session = requests.session()
        login_page = session.get("https://www.videotron.com/client/residentiel/Espace-client")

        post_values = {}
        for (input_name, input_value) in re.findall(self.PATTERN_INPUT_HIDDEN, login_page.text):
            post_values[input_name] = input_value
        post_values['userIdCookieEnabled'] = 'true'
        post_values['codeUtil'] = self.config['username']
        post_values['motDePasse'] = self.config['password']

        result_login_page = session.post("https://www.videotron.com/client/user-management/residentiel/secur/Login.do", data=post_values)

        # TODO check if login was successful

        internet_bandwidth_page = session.get("https://www.videotron.com/client/residentiel/secur/ConsommationInternet.do?locale=en")

        current_monthly_usage, maximum_monthly_usage = re.findall(self.PATTERN_MONTHLY_INTERNET_USAGE, internet_bandwidth_page.text)[0]
        days_remaining = re.findall(self.PATTERN_DAYS_IN_MONTH_REMAINING, internet_bandwidth_page.text)[0]

        return {
            'usage': current_monthly_usage,
            'maximum': maximum_monthly_usage,
            'days_remaining': days_remaining
        }