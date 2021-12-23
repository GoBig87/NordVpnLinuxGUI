from subprocess import Popen, PIPE
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
        self.country_dict = {}
        self._build_country_dict()

    def _build_country_dict(self):
        self.country_dict["Albania"] = ["foo", "foo", "foo"]
        self.country_dict["Greece"] = ["foo", "foo", "foo"]
        self.country_dict["Poland"] = ["foo", "foo", "foo"]
        self.country_dict["Argentina"] = ["foo", "foo", "foo"]
        self.country_dict["Hong_Kong"] = ["foo", "foo", "foo"]
        self.country_dict["Portugal"] = ["foo", "foo", "foo"]
        self.country_dict["Australia"] = ["foo", "foo", "foo"]
        self.country_dict["Hungary"] = ["foo", "foo", "foo"]
        self.country_dict["Romania"] = ["foo", "foo", "foo"]
        self.country_dict["Austria"] = ["foo", "foo", "foo"]
        self.country_dict["Iceland"] = ["foo", "foo", "foo"]
        self.country_dict["Belgium"] = ["foo", "foo", "foo"]
        self.country_dict["India"] = ["foo", "foo", "foo"]
        self.country_dict["Singapore"] = ["foo", "foo", "foo"]
        self.country_dict["Bosnia_And_Herzegovina"] = ["foo", "foo", "foo"]
        self.country_dict["Indonesia"] = ["foo", "foo", "foo"]
        self.country_dict["Slovakia"] = ["foo", "foo", "foo"]
        self.country_dict["Brazil"] = ["foo", "foo", "foo"]
        self.country_dict["Ireland"] = ["foo", "foo", "foo"]
        self.country_dict["Slovenia"] = ["foo", "foo", "foo"]
        self.country_dict["Bulgaria"] = ["foo", "foo", "foo"]
        self.country_dict["Israel"] = ["foo", "foo", "foo"]
        self.country_dict["South_Africa"] = ["foo", "foo", "foo"]
        self.country_dict["Canada"] = ["foo", "foo", "foo"]
        self.country_dict["Italy"] = ["foo", "foo", "foo"]
        self.country_dict["Chile"] = ["foo", "foo", "foo"]
        self.country_dict["Japan"] = ["foo", "foo", "foo"]
        self.country_dict["Spain"] = ["foo", "foo", "foo"]
        self.country_dict["Costa_Rica"] = ["foo", "foo", "foo"]
        self.country_dict["Latvia"] = ["foo", "foo", "foo"]
        self.country_dict["Croatia"] = ["foo", "foo", "foo"]
        self.country_dict["Lithuania"] = ["foo", "foo", "foo"]
        self.country_dict["Switzerland"] = ["foo", "foo", "foo"]
        self.country_dict["Cyprus"] = ["foo", "foo", "foo"]
        self.country_dict["Luxembourg"] = ["foo", "foo", "foo"]
        self.country_dict["Czech_Republic"] = ["foo", "foo", "foo"]
        self.country_dict["Taiwan"] = ["foo", "foo", "foo"]
        self.country_dict["Cyprus"] = ["foo", "foo", "foo"]
        self.country_dict["Malaysia"] = ["foo", "foo", "foo"]
        self.country_dict["Thailand"] = ["foo", "foo", "foo"]
        self.country_dict["Denmark"] = ["foo", "foo", "foo"]
        self.country_dict["Mexico"] = ["foo", "foo", "foo"]
        self.country_dict["Turkey"] = ["foo", "foo", "foo"]
        self.country_dict["Estonia"] = ["foo", "foo", "foo"]
        self.country_dict["Moldova"] = ["foo", "foo", "foo"]
        self.country_dict["Ukraine"] = ["foo", "foo", "foo"]
        self.country_dict["Finland"] = ["foo", "foo", "foo"]
        self.country_dict["Netherlands"] = ["foo", "foo", "foo"]
        self.country_dict["United_Kingdom"] = ["foo", "foo", "foo"]
        self.country_dict["France"] = ["foo", "foo", "foo"]
        self.country_dict["New_Zealand"] = ["foo", "foo", "foo"]
        self.country_dict["United_States"] = ["foo", "foo", "foo"]
        self.country_dict["Georgia"] = ["foo", "foo", "foo"]
        self.country_dict["North_Macedonia"] = ["foo", "foo", "foo"]
        self.country_dict["Germany"] = ["foo", "foo", "foo"]
        self.country_dict["Vietnam"] = ["foo", "foo", "foo"]
        self.country_dict["Norway"] = ["foo", "foo", "foo"]

    def account(self, success_cb, error_cb):
        cmd = f"{self._base_cmd} {self._account}"
        self._send_command(cmd, success_cb, error_cb)

    def check_login(self, output):
        print(output)
        if "You are not logged in." not in output:
            self.logged_in = True

    def connect_to_country(self, country):
        cmd = f"{self._base_cmd} {self._connect} {country}"
        self._send_command(cmd, self._base_success_cb, self._base_error_cb)

    def connect_to_city(self, city):
        cmd = f"{self._base_cmd} {self._connect} {city}"
        self._send_command(cmd, self._base_success_cb, self._base_error_cb)

    def login(self, success_cb, error_cb):
        cmd = f"{self._base_cmd} {self._login}"
        self._send_command(cmd, success_cb, error_cb)

    def login_success(self, output):
        print(output)
        if output == "You are already logged in.":
            pass
        else:
            url = output.split("Continue in the browser: ")[1]
            print(url)
            webbrowser.open(url)

    def _base_error_cb(self, error_cb):
        pass

    def _base_success_cb(self, error_cb):
        pass

    def _send_command(self, cmd, success_cb, error_cb):
        print(cmd)
        process = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
        output, error = process.communicate()
        if error:
            error_cb(str(error.decode("utf-8") ))
        else:
            success_cb(str(output.decode("utf-8")))