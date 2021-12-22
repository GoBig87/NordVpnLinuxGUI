from subprocess import Popen, PIPE
from threading import Thread
import webbrowser


class NordClient(object):
    def __init__(self):
        self.logged_in = False
        self.cancel_login = False
        self._base_cmd = "nordvpn"
        self._account = "account"
        self._cities = "cities"
        self._connect = "connect"
        self._countries = "countries"
        self._disconnect = "disconnect"
        self._groups = "groups"
        self._login = "login"
        self._logout = "logout"
        self._rate = "rate"
        self._register = "register"
        self._set = "set"
        self._settings = "settings"
        self._status = "status"
        self._whitelist = "whitelist"
        self._help = "help"
        self._version = "version"

    def account(self, success_cb, error_cb):
        cmd = [self._base_cmd, self._account]
        self._send_command(cmd, success_cb, error_cb)

    def check_login(self, output):
        if output != "You are not logged in.":
            self.logged_in = True

    def login(self, success_cb, error_cb):
        cmd = [self._base_cmd, self._login]
        self._send_command(cmd, success_cb, error_cb)

    def _login_success(self, output):
        if output == "You are already logged in.":
            pass
        else:
            url = output.split("http")[0]
            webbrowser.open(url)

    def _base_error_cb(self, error_cb):
        pass

    def _send_command(self, cmd, success_cb, error_cb):
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        output, error = process.communicate()
        if error:
            error_cb(error)
        else:
            success_cb(output)