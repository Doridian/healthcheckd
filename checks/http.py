from .base import BaseCheck
from requests import get, head

class HTTPCheck(BaseCheck):
    def __init__(self, config):
        super().__init__(config)

        self.url = config.get('url', 'http://127.0.0.1/')
        self.host_override = config.get('host_override', '')
        method_str = config.get('method', 'GET').upper()
        if method_str == 'GET':
            self.method = get
        elif method_str == 'HEAD':
            self.method = head
        else:
            raise ValueError('Invalid method. Supports GET and HEAD')

        self.status_codes = set(map(int, config.get('statusCodes', '200,201,202,204').split(',')))

    def check(self):
        headers = {}
        if self.host_override != '':
            headers['host'] = self.host_override
        res = self.method(self.url, headers=headers)
        return res.status_code in self.status_codes
