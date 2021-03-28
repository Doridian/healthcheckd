from .base import BaseCheck

presets = {
    'wsrep': {
        'query': 'SHOW STATUS WHERE variable_name = "wsrep_ready"',
        'expect': 'ON',
    },
    'simple': {
        'query': 'SELECT 1+1',
        'expect': '2'
    },
}

class MySQLCheck(BaseCheck):
    def __init__(self, config):
        super().__init__(config)
        
        self.host = config.get('host', '127.0.0.1')
        self.port = config.getint('port', 3306)
        self.user = config.get('user', 'root')
        self.password = config.get('password', '')

        presetStr = config.get('preset', 'simple')
        preset = presets[presetStr]

        self.query = config.get('query', preset['query'])
        self.expect = config.get('expect', preset['expect'])
