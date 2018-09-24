import os
import logging
from ConfigParser import ConfigParser, NoOptionError, NoSectionError


class UserManager:
    users = {}
    users_path = ""
    logger = None

    def __init__(self, users_path):
        self.users_path = users_path
        self.logger = logging.getLogger('vk_bot_application.userManager')
        if not os.path.exists(self.users_path):
            self.create_config()

        self.load_users()

    def create_config(self):
        config = ConfigParser()
        config.add_section("Users")

        with open(self.users_path, "w") as config_file:
            config.write(config_file)

    def add_user_parameters(self, number, user_id, allow, blocked, fio, time):
        d = {'number': int(number), 'user_id': int(user_id), 'allow': int(allow), 'blocked': int(blocked), 'fio': fio, 'time': time}
        self.users[int(user_id)] = d

    def load_users(self):
        config = ConfigParser()
        config.read(self.users_path)
        # TODO fix set user number
        count = 0
        while True:
            try:
                user_number = "user_{0}".format(count)
                user_string = config.get("Users", user_number)

                arr = user_string.split(";")
                self.add_user_parameters(count, arr[0], arr[1], arr[2], arr[3], arr[4])
                count = count + 1

            except NoOptionError:
                break

    def has_user(self, user_id):
        for vk_id in self.users:
            if int(vk_id) == int(user_id):
                return True

        return False

    def save_users(self):
        config = ConfigParser()
        config.add_section("Users")

        for vk_id in self.users:
            user = self.users[vk_id]
            fio = user['fio']
            number = user['number']
            user_id = user['user_id']
            allow = user['allow']
            blocked = user['blocked']
            time = user['time']
            user_str = "{0};{1};{2};{3};{4}".format(user_id, allow, blocked, fio, time)
            config.set("Users", "user_{0}".format(number), user_str)

        with open(self.users_path, "w") as config_file:
            config.write(config_file)

    def get_next_index(self):
        return len(self.users)

    def get_user_property(self, user_id, property_name):
        for vk_id in self.users:
            if int(vk_id) == int(user_id):
                user = self.users[vk_id]
                property_value = None
                try:
                    property_value = user[property_name]
                except KeyError:
                    self.logger.info("getUserProperty : property {0} was not found for user {1}".format(property_name, user_id))
                return property_value

        self.logger.info("getUserProperty : user {0} was not found!".format(user_id))
        return None

    def set_user_property(self, user_id, property_name, value):
        for vk_id in self.users:
            user = self.users[vk_id]
            if int(vk_id) == int(user_id):
                user[property_name] = value
                return user

        self.logger.info("setUserProperty: user {0} was not found!".format(user_id))
        return None

    def add_user(self, user_id, allow, blocked, fio, time=""):
        for vk_id in self.users:
            if int(user_id) == int(vk_id):
                self.logger.info("user with: vk_id {0} already exists!".format(user_id))
                return False
        index = self.get_next_index()
        self.add_user_parameters(index, user_id, allow, blocked, fio, time)

    def get_users(self):
        return self.users
