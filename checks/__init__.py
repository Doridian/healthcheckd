from .http import HTTPCheck
from .file import FileCheck
from .mysql import MySQLCheck

checks = {
    'http': HTTPCheck,
    'file': FileCheck,
    'mysql': MySQLCheck,
}

def loadCheck(config):
    check_type = config.get('type', '').lower()
    CheckCls = checks[check_type]
    return CheckCls(config)
