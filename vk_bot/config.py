import os
import logging
import sys
from ConfigParser import ConfigParser, NoOptionError, NoSectionError


class Config:
    VK_GROUP_ACCESS_TOKEN = None
    VK_API_ENDPOINT = None
    VK_API_VERSION = None
    VK_GROUP_ID = None
    LOG_FILE = None
    USERS_FILE = None

    TEMPLATE_VK_ACCESS_TOKEN = "<GROUP_ACCESS_TOKEN>"
    TEMPLATE_VK_GROUP_ID = "<GROUP_ID>"

    config_path = None
    logger = None

    def __init__(self, config_path):
        self.config_path = config_path
        self.load_config()
        self.logger = logging.getLogger('vk_bot_application.config')

    def load_config(self):
        config = self.get_config()
        try:
            self.VK_GROUP_ACCESS_TOKEN = config.get("VK_Settings", "access_token")
            self.VK_API_VERSION = config.get("VK_Settings", "api_version")
            self.VK_GROUP_ID = config.get("VK_Settings", "group_id")
            self.VK_API_ENDPOINT = config.get("VK_Settings", "api_endpoint")
            self.LOG_FILE = config.get("Log", "logfile")
            self.USERS_FILE = config.get("Users", "usersfile")
        except NoSectionError as e:
            msg = "Load config error : {0}".format(e)
            print msg
        except NoOptionError as e:
            msg = "Load config error : {0}".format(e)
            print msg

    def verify_config(self):
        if self.VK_GROUP_ACCESS_TOKEN == self.TEMPLATE_VK_ACCESS_TOKEN:
            msg = "you should define access_token variable in configs ('{0}' file)".format(self.config_path)
            self.logger.warn(msg)
            print msg
            sys.exit(1)

        if self.VK_GROUP_ID == self.TEMPLATE_VK_GROUP_ID:
            msg = "you should define group_id variable in configs ('{0}' file)".format(self.config_path)
            self.logger.warn(msg)
            print msg
            sys.exit(1)

    def get_config(self):
        if not os.path.exists(self.config_path):
            self.create_config()

        config = ConfigParser()
        config.read(self.config_path)
        return config

    def create_config(self):
        config = ConfigParser()
        config.add_section("VK_Settings")
        config.set("VK_Settings", "access_token", self.TEMPLATE_VK_ACCESS_TOKEN)
        config.set("VK_Settings", "api_version", "5.80")
        config.set("VK_Settings", "group_id", self.TEMPLATE_VK_GROUP_ID)
        config.set("VK_Settings", "api_endpoint", "https://api.vk.com/method/")

        config.add_section("Log")
        config.set("Log", "logfile", "vk_bot.log")

        config.add_section("Users")
        config.set("Users", "usersfile", "users.data")

        with open(self.config_path, "w") as config_file:
            config.write(config_file)
