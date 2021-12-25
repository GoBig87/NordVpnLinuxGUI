from subprocess import Popen, PIPE
import webbrowser


class NordClient(object):
    def __init__(self):
        self.account_information = ""
        self.email = ""
        self.vpn_service = ""
        self.status_dict = {}
        self.version = ""
        self.country_dict = {}
        self.group_list = []
        self.settings_dict = {}
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
        self._build_country_dict()
        self._build_groups()
        self.get_settings()
        self.get_account_info()
        self.get_status()
        self.get_version()

    def _build_groups(self):
        cmd = f"{self._base_cmd} {self._groups}"
        self._send_command(cmd, self._build_groups_resp, self._base_error_cb)

    def _build_groups_resp(self, output):
        group_list = output.replace(",", "").split()
        group_list = list(filter(('-').__ne__, group_list))
        self.group_list = group_list

    def _build_country_dict(self):
        cmd = f"{self._base_cmd} {self._countries}"
        self._send_command(cmd, self._build_country_dict_resp, self._base_cmd)

    def _build_country_dict_resp(self, output):
        country_list = output.replace(",", "").split()
        country_list = list(filter(('-').__ne__, country_list))
        for country in country_list:
            cmd = f"{self._base_cmd} {self._cities} {country}"
            outs, err = self._send_dir_command(cmd)
            city_list = []
            if outs:
                city_list = outs.split()
            city_list = list(filter(('-').__ne__, city_list))
            self.country_dict[country] = city_list

    def get_version(self):
        cmd = f"{self._base_cmd} {self._version}"
        self._send_command(cmd, self.get_version_resp, self._base_error_cb)

    def get_version_resp(self, output):
        self.version = output

    def get_status(self):
        cmd = f"{self._base_cmd} {self._status}"
        self._send_command(cmd, self.get_status_resp, self._base_error_cb)

    def get_status_resp(self, output):
        rsp_list = output.split("\n")
        for item in rsp_list:
            if item:
                key, value = item.split(":")
                key_list = key.split()
                key_list = list(filter(('-').__ne__, key_list))
                self.status_dict[key_list[0]] = value

    def get_settings(self):
        cmd = f"{self._base_cmd} {self._settings}"
        self._send_command(cmd, self.get_settings_resp, self._base_error_cb)

    def get_settings_resp(self, output):
        rsp_list = output.split("\n")
        for item in rsp_list:
            if item:
                key, value = item.split(":")
                key_list = key.split()
                key_list = list(filter(('-').__ne__, key_list))
                self.settings_dict[key_list[0]] = value

    def get_account_info(self):
        cmd = f"{self._base_cmd} {self._account}"
        self._send_command(cmd, self._parse_account_rsp, self._base_error_cb)

    def _parse_account_rsp(self, output):
        try:
            rsp_list = output.split("\n")
            self.account_information = rsp_list[0].split("Account Information:")[-1]
            self.email = rsp_list[1].split("Email Address: ")[-1]
            self.vpn_service = rsp_list[2].split("VPN Service: ")[-1]
        except:
            self.account_information = ""
            self.email = ""
            self.vpn_service = ""

    def account(self, success_cb, error_cb):
        cmd = f"{self._base_cmd} {self._account}"
        self._send_command(cmd, success_cb, error_cb)

    def check_login(self, output):
        print(output)
        if "You are not logged in." not in output:
            self.logged_in = True

    def connect(self, selection, success_cb, error_cb):
        cmd = f"{self._base_cmd} {self._connect} {selection}"
        self._send_command(cmd, success_cb, error_cb)

    def connect_to_country(self, country, success_cb, error_cb):
        cmd = f"{self._base_cmd} {self._connect} {country}"
        self._send_command(cmd, success_cb, error_cb)

    def connect_to_city(self, city, success_cb, error_cb):
        cmd = f"{self._base_cmd} {self._connect} {city}"
        self._send_command(cmd, success_cb, error_cb)

    def quick_connect(self, success_cb, error_cb):
        cmd = f"{self._base_cmd} {self._connect}"
        self._send_command(cmd, success_cb, error_cb)

    def disconnect(self, success_cb, error_cb):
        cmd = f"{self._base_cmd} {self._disconnect}"
        self._send_command(cmd, success_cb, error_cb)

    def login(self, success_cb, error_cb):
        cmd = f"{self._base_cmd} {self._login}"
        self._send_command(cmd, success_cb, error_cb)

    def logout(self, success_cb, error_cb):
        cmd = f"{self._base_cmd} {self._logout}"
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
        print(error_cb)
        pass

    def _base_success_cb(self, error_cb):
        pass

    def _send_dir_command(self, cmd):
        process = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
        output, error = process.communicate()
        return output.decode("utf-8"), error.decode("utf-8")

    def _send_command(self, cmd, success_cb, error_cb):
        print(cmd)
        process = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
        output, error = process.communicate()
        if error:
            error_cb(str(error.decode("utf-8")))
        else:
            success_cb(str(output.decode("utf-8")))