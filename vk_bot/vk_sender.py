# -*- coding: utf-8 -*-
import datetime
import random  # tmp

from config import Config
from log import Log
from user_manager import UserManager
from vkapi import VkApi


class VKBotApplication:
    cfg = None
    logger = None
    botAPI = None
    uManager = None

    def __init__(self, path):
        self.cfg = Config(path)
        self.logger = Log.get_logger(self.cfg.LOG_FILE)
        self.cfg.verify_config()
        self.botAPI = VkApi(self.cfg)
        self.uManager = UserManager()
        self.logger.info("VKBot started")

    def get_members(self):
        self.logger.info("getting_members")
        r = self.botAPI.get_members_list()
        # count = int(r['response']['count'])
        member_user_ids = r['response']['items']

        # check if users in memory
        for user_id in member_user_ids:
            # new user detected
            if not self.uManager.has_user(user_id):
                # TODO try/catch
                # TODO multiple list
                user_info = self.get_user_info(user_id)
                first_name = user_info['response'][0]['first_name'].encode("utf-8")
                last_name = user_info['response'][0]['last_name'].encode("utf-8")
                self.uManager.add_user(user_id, -1, 0, "{0} {1}".format(first_name, last_name), "")

        self.logger.info("members are {0}".format(member_user_ids))
        return member_user_ids

    def check_allowed_receive_message(self, member_user_ids):
        self.logger.info("Check allowed receive message")
        allowed_members = []
        for member_user_id in member_user_ids:
            r = self.botAPI.is_messages_from_group_allowed(member_user_id)
            if r['response']['is_allowed'] == 1:
                self.uManager.set_user_property(member_user_id, "allow", 1)
                allowed_members.append(member_user_id)
            else:
                self.uManager.set_user_property(member_user_id, "allow", 0)
                time = self.uManager.get_user_property(member_user_id, "time")
                if time is None or time == "":
                    # try send message first time anyway
                    allowed_members.append(member_user_id)

        self.logger.info("Allowed members are : {0}".format(allowed_members))
        return allowed_members

    def skip_blocked_users(self, user_ids):
        non_blocked = []
        for user_id in user_ids:
            if self.uManager.get_user_property(user_id, "blocked") == 0:
                non_blocked.append(user_id)

        self.logger.info("Non blocked users : {0}".format(non_blocked))
        return non_blocked

    def get_user_info(self, user_id):
        self.logger.info("Get user {0} info".format(user_id))
        r = self.botAPI.get_user_info(user_id)
        return r

    def send_message(self, message, user_ids):
        cap = 100
        msg = "{0} : {1}".format(random.randint(0, 1000), message)
        if not user_ids:
            self.logger.info("no user to send message")
            return

        batch_users = []

        if len(user_ids) > 1:
            for user_id in user_ids:
                batch_users.append(user_id)
                if len(batch_users) == cap:
                    user_ids_str = ','.join(str(e) for e in batch_users)
                    self.botAPI.send_messages(msg, user_ids_str)
                    batch_users = []

            if len(batch_users) > 0:
                user_ids_str = ','.join(str(e) for e in batch_users)
                self.botAPI.send_messages(msg, user_ids_str)
        else:
            self.botAPI.send_message(msg, user_ids[0])

        time = datetime.datetime.now().strftime("%d %B %Y %I:%M%p")
        for user_id in user_ids:
            self.uManager.set_user_property(user_id, "time", time)

        self.uManager.save_users()


if __name__ == "__main__":
    setting_path = "settings.cfg"
    message_to_send = "This is a test message to send"

    app = VKBotApplication(setting_path)

    members_id = app.get_members()
    non_blocked_users = app.skip_blocked_users(members_id)
    allowedMembers = app.check_allowed_receive_message(non_blocked_users)

    app.send_message(message_to_send, allowedMembers)
