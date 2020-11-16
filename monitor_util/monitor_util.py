import requests
import logging
import json


class MonitorUtil(object):
    url = None
    token = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(MonitorUtil, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

    @staticmethod
    def init_with_json_config(__config_file_path__):
        monitor_json = json.load(open(__config_file_path__, 'r'))
        monitor_util = MonitorUtil()
        monitor_util.url = monitor_json['url']
        monitor_util.token = monitor_json['token']

    @staticmethod
    async def update_status(key_name, value):
        monitor = MonitorUtil()
        req = requests.post(
            url=monitor.url,
            data={
                'token': monitor.token,
                'key': key_name,
                'value': value
            }
        )
        logging.info(req.text)
