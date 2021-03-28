from .base import BaseCheck
from os.path import exists

class FileCheck(BaseCheck):
    def __init__(self, config):
        super().__init__(self, config)

        self.path = config.get('path', '/')
        self.exists = config.getbool('exists', True)

    def check(self):
        return exists(self.path) == self.exists
