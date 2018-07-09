import requests
import urllib
import logging


class VkApi:
    cfg = None
    logger = None

    def __init__(self, cfg):
        self.cfg = cfg
        self.logger = logging.getLogger('vk_bot_application.vk_api')

    def request_has_error(self, res):
        try:
            error = res.json()['error'] is None
        except KeyError:
            error = None

        return error

    def vk_api_call(self, method_name, params=None):
        # TODO in case of error return value
        if params is None:
            params = {}

        params['access_token'] = self.cfg.VK_GROUP_ACCESS_TOKEN
        params['v'] = self.cfg.VK_API_VERSION
        query = urllib.urlencode(params)
        url = self.cfg.VK_API_ENDPOINT + method_name + "?" + query
        headers = {'Content-Type': 'application/json'}
        self.logger.info("request is : {0}".format(url))

        res = requests.get(url, headers=headers)
        error = self.request_has_error(res)
        if error is None:
            return res.json()
        else:
            error = res.json()['error']
            msg = "Error in request {0}: {2} (error_code is {1})".format(method_name, error['error_code'], error['error_msg'])
            self.logger.warning(msg)

    def get_members_list(self):
        return self.vk_api_call("groups.getMembers", {"group_id": self.cfg.VK_GROUP_ID})
        # return {u'response': {u'count': 3, u'items': [111, 123321, 987789]}}

    def is_messages_from_group_allowed(self, user_id):
        return self.vk_api_call("messages.isMessagesFromGroupAllowed", {"group_id": self.cfg.VK_GROUP_ID, "user_id": user_id})
        # import random
        # msg = {u'response': {u'is_allowed': random.randint(0, 1)}}
        # return msg

    def send_message(self, message, user_id):
        self.logger.info("sending message to {0}".format(user_id))
        # return self.vk_api_call("messages.send", {"message": message, "user_id": user_id})
        return "ok"

    def get_user_info(self, user_id):
        return self.vk_api_call("users.get", {"user_ids": user_id})
        # return {u'response': [{u'first_name': u'\u0410\u043d\u0434\u0440\u0435\u0439', u'last_name': u'\u0410\u0440\u0442\u0435\u043c\u044c\u0435\u0432', u'id': 111}]}
