import requests
import re
import datetime


class Videotron:
    PATTERN_INPUT_HIDDEN = re.compile(r"<input type=\"hidden\" name=\"(?P<tokenName>\w+)\" value=\"(?P<tokenValue>[\w.]+)\">")
    PATTERN_MONTHLY_INTERNET_USAGE = re.compile(r"<span class=\"quantities\">(?P<current>[\d.]+) / (?P<maximum>[\d.]+).*(?P<unit>GB|MB)</span>")
    PATTERN_DAYS_IN_MONTH_REMAINING = re.compile(r"<p class=\"note_reset\">Number of days before reverting to zero: (?P<daysLeft>\d+) days?</p>")
    PATTERN_LAST_UPDATE = re.compile(r"<p class=\"details_mise_a_jour\">(?P<last_update>Last updated \w+ (?P<last_update_date>\w+ \d+, \d+) at (?P<last_update_time>\d+:\d+ \w+))</p>")

    def __init__(self, config):
        self.config = config

    def get_current_month_usage(self):
        session = requests.session()

        if not (self._login(session)):
            raise RuntimeError('Login failed!')

        bandwidth_page = session.get("https://www.videotron.com/client/residentiel/secur/ConsommationInternet.do?locale=en")

        update_date = self._get_update_date(bandwidth_page)
        current_monthly_usage, maximum_monthly_usage, unit = self._get_bandwidth_usage(bandwidth_page)
        days_remaining = self._get_days_remaining(bandwidth_page)

        self._logout(session)
        session.close()

        return {
            'update_date': update_date,
            'usage': current_monthly_usage,
            'maximum': maximum_monthly_usage,
            'unit': unit,
            'days_remaining': days_remaining
        }

    def _login(self, session):
        login_page = session.get("https://www.videotron.com/client/residentiel/Espace-client")

        post_values = {}
        for (input_name, input_value) in re.findall(self.PATTERN_INPUT_HIDDEN, login_page.text):
            post_values[input_name] = input_value
        post_values['userIdCookieEnabled'] = 'true'
        post_values['codeUtil'] = self.config['username']
        post_values['motDePasse'] = self.config['password']

        result_login_page = session.post("https://www.videotron.com/client/user-management/residentiel/secur/Login.do", data = post_values)

        return True  # TODO check if login was successful

    def _get_update_date(self, bandwidth_page):
        last_update, last_update_date, last_update_time = re.findall(self.PATTERN_LAST_UPDATE, bandwidth_page.text)[0]

        return datetime.datetime.strptime(last_update_date + " " + last_update_time, '%B %d, %Y %I:%M %p').strftime('%Y-%m-%d %H:%M')

    def _get_bandwidth_usage(self, bandwidth_page):
        return re.findall(self.PATTERN_MONTHLY_INTERNET_USAGE, bandwidth_page.text)[0]  # TODO handle possible errors

    def _get_days_remaining(self, bandwidth_page):
        return re.findall(self.PATTERN_DAYS_IN_MONTH_REMAINING, bandwidth_page.text)[0]  # TODO handle possible errors

    def _logout(self, session):
        session.get("https://www.videotron.com/client/user-management/residentiel/secur/Logout.do?dispatch=logout")  # TODO check if logout was successful
