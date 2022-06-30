from subprocess import Popen, PIPE
from threading import Thread
import webbrowser
import re


MESH_WARNING = "New feature - Meshnet! Link remote devices in Meshnet to connect " \
               "to them directly over encrypted private tunnels, and route your " \
               "traffic through another device. Use the `nordvpn meshnet --help` " \
               "command to get started. Learn more: https://nordvpn.com/features/meshnet/\n"


class NordClient(object):
    def __init__(self, error_cb=None):
        if error_cb:
            self.error_cb = error_cb
        else:
            self.error_cb = self._base_error
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
        self._add = "add"
        self._all = "all"
        self._cities = "cities"
        self._connect = "connect"
        self._countries = "countries"
        self._disable = "disable"
        self._disconnect = "disconnect"
        self._dns = "dns"
        self._enable = "enable"
        self._groups = "groups"
        self._login = "login"
        self._logout = "logout"
        self._rate = "rate"
        self._register = "register"
        self._remove = "remove"
        self._port = "port"
        self._protocol = "protocol"
        self._set = "set"
        self._settings = "settings"
        self._status = "status"
        self._subnet = "subnet"
        self._technology = "technology"
        self._whitelist = "whitelist"
        self._help = "help"
        self._version = "version"
        self.get_countries()
        self.get_groups()
        self.get_settings()
        self.get_account_info()
        self.get_status()
        self.get_version()

    def add_whitelist_subnet(self, subnet, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._whitelist} {self._add} {self._subnet} {subnet}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self._base_success_cb(), self._base_error_cb)

    def add_whitelist_port(self, port, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._whitelist} {self._add} {self._port} {port}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self._base_success_cb(), self._base_error_cb)

    def get_groups(self, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._groups}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self.get_groups_resp, self._base_error_cb)

    def get_groups_resp(self, output):
        print(f"hello {output}")
        if "Please check your internet connection and try again." in output:
            self.error_cb("", output)
            return []
        try:
            group_list = output.replace(",", "").split()
            group_list = list(filter(('-').__ne__, group_list))
            self.group_list = group_list
        except:
            self.error_cb("Failed to parse group.  Found: ", output)
        return group_list

    def get_countries(self, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._countries}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self.get_countries_resp, self._base_error_cb)

    def get_countries_resp(self, output):
        if "Please check your internet connection and try again." in output:
            self.error_cb("", output)
            return self.country_dict
        try:
            country_list = output.replace(",", "").split()
            country_list = list(filter(('-').__ne__, country_list))
            for country in country_list:
                cmd = f"{self._base_cmd} {self._cities} {country}"
                outs, err = self._send_dir_command(cmd)
                city_list = []
                if outs:
                    city_list = outs.replace(",", "").split()
                city_list = list(filter(('-').__ne__, city_list))
                self.country_dict[country] = city_list
        except:
            self.error_cb("Failed to parse Country list.  Found: ", output)
        return self.country_dict

    def get_version(self, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._version}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self.get_version_resp, self._base_error_cb)

    def get_version_resp(self, output):
        if "Please check your internet connection and try again." in output:
            self.error_cb("", output)
            return ""
        self.version = output
        return self.version

    def get_status(self, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._status}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self.get_status_resp, self._base_error_cb)

    def get_status_resp(self, output):
        if "Please check your internet connection and try again." in output:
            self.error_cb("", output)
            return self.status_dict
        try:
            rsp_list = output.split("\n")
            for item in rsp_list:
                if item:
                    key, value = item.split(":")
                    key_list = key.split()
                    key_list = list(filter(('-').__ne__, key_list))
                    if len(key_list) > 1:
                        key_list = [f"{key_list[0]}_{key_list[1]}"]
                    self.status_dict[key_list[0]] = value
        except:
            self.error_cb("Failed to parse Status.  Found: ", output)
        return self.status_dict

    def get_settings(self, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._settings}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self.get_settings_resp, self._base_error_cb)

    def get_settings_resp(self, output):
        self.settings_dict = {}
        self.settings_dict["Whitelisted_subnets"] = []
        self.settings_dict["Whitelisted_ports"] = []
        if "Please check your internet connection and try again." in output:
            self.error_cb("", output)
            return self.settings_dict
        try:
            rsp_list = output.split("\n")
            for item in rsp_list:
                if "Whitelisted" in item:
                    pass
                elif ":" in item:
                    key, value = item.split(":")
                    key.replace(" ", "_")
                    key_list = key.split()
                    key_list = list(filter(('-').__ne__, key_list))
                    if len(key_list) > 1:
                        key_list = [f"{key_list[0]}_{key_list[1]}"]
                    self.settings_dict[key_list[0]] = value.replace(" ", "")
                elif re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", item.strip()):
                    self.settings_dict["Whitelisted_subnets"].append(item.strip())
                elif re.match(r"\d{1,6}", item.strip().replace("(UDP|TCP)", "")):
                    self.settings_dict["Whitelisted_ports"].append(item.strip())
        except:
            self.error_cb("Failed to parse Settings.  Found: ", output)
        return self.settings_dict

    def get_account_info(self, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._account}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self.get_account_rsp, self._base_error_cb)

    def get_account_rsp(self, output):
        if "You are not logged in." not in output:
            self.logged_in = True
        else:
            return None, None, None
        try:
            rsp_list = output.split("\n")
            self.account_information = rsp_list[0].split("Account Information:")[-1]
            self.email = rsp_list[1].split("Email Address: ")[-1]
            self.vpn_service = rsp_list[2].split("VPN Service: ")[-1]
        except:
            self.account_information = ""
            self.email = ""
            self.vpn_service = ""
        return self.account_information, self.email, self.vpn_service

    def connect(self, selection, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._connect} {selection}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self.connect_rsp, self._base_error_cb)

    def connect_rsp(self, output):
        pass

    def connect_to_country(self, country, success_cb, error_cb):
        cmd = f"{self._base_cmd} {self._connect} {country}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self.connect_rsp, self._base_error_cb)

    def connect_to_city(self, city, success_cb, error_cb):
        cmd = f"{self._base_cmd} {self._connect} {city}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self.connect_rsp, self._base_error_cb)

    def quick_connect(self, success_cb, error_cb):
        cmd = f"{self._base_cmd} {self._connect}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self.connect_rsp, self._base_error_cb)

    def disconnect(self, success_cb, error_cb):
        cmd = f"{self._base_cmd} {self._disconnect}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self.disconnect_rsp, self._base_error_cb)

    def disconnect_rsp(self, output):
        pass

    def login(self, success_cb, error_cb):
        cmd = f"{self._base_cmd} {self._login}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self.login_success, self._base_error_cb)

    def login_rsp(self, output):
        if "You are not logged in." not in output:
                self.logged_in = True

    def logout(self, success_cb, error_cb):
        cmd = f"{self._base_cmd} {self._logout}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self.login_rsp, self._base_error_cb)

    def login_success(self, output):
        if output == "You are already logged in.":
            pass
        else:
            url = output.split("Continue in the browser: ")[1]
            webbrowser.open(url)

    def _base_error_cb(self, error_cb):
        print(error_cb)
        pass

    def _base_success_cb(self, error_cb):
        pass

    def remove_all_whitelist(self, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._whitelist} {self._remove} {self._all}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self._base_success_cb(), self._base_error_cb)

    def remove_all_whitelist_port(self, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._whitelist} {self._remove} {self._port} {self._all}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self._base_success_cb(), self._base_error_cb)

    def remove_all_whitelist_subnet(self, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._whitelist} {self._remove} {self._subnet} {self._all}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self._base_success_cb(), self._base_error_cb)

    def remove_whitelist_port(self, port, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._whitelist} {self._remove} {self._port} {port}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self._base_success_cb(), self._base_error_cb)

    def remove_whitelist_subnet(self, subnet, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._whitelist} {self._remove} {self._subnet} {subnet}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self._base_success_cb(), self._base_error_cb)

    def _send_dir_command(self, cmd):
        process = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
        output, error = process.communicate()
        return output.decode("utf-8").replace(MESH_WARNING, ''), error.decode("utf-8")

    def _send_command(self, *args):
        cmd = args[0]
        print(f"Sending Command: {cmd}")
        success_cb = args[1]
        error_cb = args[2]
        process = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
        output, error = process.communicate()
        if error:
            print(f"Error: {str(error.decode('utf-8'))}")
            error_cb(str(error.decode("utf-8")))
        else:
            print(f"{str(output.decode('utf-8')).replace(MESH_WARNING, '')}")
            success_cb(str(output.decode("utf-8").replace(MESH_WARNING, '')))

    def set_dns(self, dns, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._set} {self._dns} {dns}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self._base_success_cb, self._base_error_cb)

    def set_setting_enabled(self, setting, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._set} {setting} {self._enable}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self._base_success_cb, self._base_error_cb)

    def set_setting_disabled(self, setting, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._set} {setting} {self._disable}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self._base_success_cb, self._base_error_cb)

    def set_protocol(self, protocol, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._set} {self._protocol} {protocol}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self._base_success_cb, self._base_error_cb)

    def set_technology(self, technology, success_cb=None, error_cb=None):
        cmd = f"{self._base_cmd} {self._set} {self._technology} {technology}"
        thread = self._setup_thread(cmd, success_cb, error_cb)
        if thread:
            return thread.start()
        self._send_command(cmd, self._base_success_cb, self._base_error_cb)

    def _setup_thread(self, cmd, succes_cb, error_cb):
        thread = None
        if succes_cb:
            thread = Thread(target=self._send_command, args=(cmd, succes_cb, error_cb))
        return thread

    def _base_error(self, error):
        print(error)