from .base import BaseCheck
from os.path import exists

class FileCheck(BaseCheck):
    def __init__(self, config):
        super().__init__(config)
        self.path = config.get('path', '/')

    def check(self):
        return exists(self.path)
