from .base import BaseCheck

class HTTPCheck(BaseCheck):
    def __init__(self, config):
        super().__init__(self, config)

        self.port = config.getint('port', 80)
        self.host = config.get('host', '127.0.0.1')

        self.path = config.get('path', '/')
        self.method = config.get('method', 'GET')

        self.statusCodes = map(int, config.get('statusCodes', '200,201,202,204').split(','))
