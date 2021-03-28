from checks import loadCheck
from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')

checks = []

for section_name in parser.sections():
    section = parser[section_name]
    section['name'] = section_name
    checks.append(loadCheck(section))

print(checks)
