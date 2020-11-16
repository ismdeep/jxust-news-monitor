import json

from telethon.sync import TelegramClient
from telethon import functions


class TelegramMsgSender(object):
    client = None
    channel = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(TelegramMsgSender, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

    @staticmethod
    def init_with_config(__config_json_path__):
        telegram_bot_config = json.load(open(__config_json_path__, 'r'))
        api_id = telegram_bot_config['api_id']
        api_hash = telegram_bot_config['api_hash']
        channel_share_link = telegram_bot_config['channel_share_link']
        sender = TelegramMsgSender()
        sender.client = TelegramClient(r"anon.session", api_id, api_hash)
        sender.client.connect()
        sender.channel = sender.client.get_entity(channel_share_link)

    @staticmethod
    def send_text_msg(__msg__, no_webpage=True):
        sender = TelegramMsgSender()
        sender.client(functions.messages.SendMessageRequest(
            peer=sender.channel,
            message=__msg__,
            no_webpage=no_webpage
        ))
