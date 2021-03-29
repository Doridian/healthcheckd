from .base import BaseCheck
from mysql import connector

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
        self.database = config.get('database', 'INFORMATION_SCHEMA')

        presetStr = config.get('preset', 'simple')
        preset = presets[presetStr]

        self.query = config.get('query', preset['query'])
        self.expect = config.get('expect', preset['expect'])

    def check(self):
        conn = connector.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
        cur = conn.cursor()
        cur.execute(self.query)
        res = cur.fetchone()
        return str(res) == self.expect
