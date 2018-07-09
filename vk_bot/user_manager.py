import os
import logging
from ConfigParser import ConfigParser, NoOptionError, NoSectionError


class UserManager:
    users = []
    users_path = "users.data"
    logger = None

    def __init__(self):
        self.logger = logging.getLogger('vk_bot_application.userManager')

        if not os.path.exists(self.users_path):
            self.create_config()

        self.load_users()

    def create_config(self):
        config = ConfigParser()
        config.add_section("Users")

        with open(self.users_path, "w") as config_file:
            config.write(config_file)

    def load_users(self):
        config = ConfigParser()
        config.read(self.users_path)

        count = 0
        while True:
            try:
                user_number = "user_{0}".format(count)
                user_string = config.get("Users", user_number)

                arr = user_string.split(";")
                d = {'number': count, 'user_id': int(arr[0]), 'allow': int(arr[1]), 'blocked': int(arr[2]), 'fio': arr[3], 'time': arr[4]}
                dd = {arr[0]: d}
                count = count + 1
                self.users.append(dd)

            except NoOptionError:
                break

    def has_user(self, user_id):
        for item in self.users:
            for vk_id in item:
                if int(vk_id) == int(user_id):
                    return True

        return False

    def save_users(self):
        config = ConfigParser()
        config.add_section("Users")

        for item in self.users:
            for vk_id in item:
                user = item[vk_id]
                fio = user['fio']
                number = user['number']
                user_id = user['user_id']
                allow = user['allow']
                blocked = user['blocked']
                time = user['time']
                str = "{0};{1};{2};{3};{4}".format(user_id, allow, blocked, fio, time)
                config.set("Users", "user_{0}".format(number), str)

        with open(self.users_path, "w") as config_file:
            config.write(config_file)

    def get_next_index(self):
        return len(self.users)

    def get_user_property(self, user_id, property_name):
        for item in self.users:
            for vk_id in item:
                if int(vk_id) == int(user_id):
                    property_value = None
                    try:
                        property_value = item[vk_id][property_name]
                    except KeyError:
                        self.logger.info("getUserProperty : property {0} was not found for user {1}".format(property_name, user_id))
                    return property_value

        self.logger.info("getUserProperty : user {0} was not found!".format(user_id))
        return None

    def set_user_property(self, user_id, property_name, value):
        for item in self.users:
            for vk_id in item:
                if int(vk_id) == int(user_id):
                    item[vk_id][property_name] = value
                    return item[vk_id]

        self.logger.info("setUserProperty: user {0} was not found!".format(user_id))
        return None

    def add_user(self, vk_id, allow, blocked, fio, time=""):
        for item in self.users:
            for key in item:
                if int(vk_id) == int(key):
                    self.logger.info("user with: vk_id {0} already exists!".format(vk_id))
                    return False
        index = self.get_next_index()

        d = {'number': index, 'user_id': vk_id, 'allow': allow, 'blocked': blocked, 'fio': fio, 'time': time}
        dd = {vk_id: d}
        self.users.append(dd)

    def get_users(self):
        return self.users
