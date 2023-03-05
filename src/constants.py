from pathlib import Path


MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_DOC_URL = 'https://peps.python.org/'

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'

# Recording time - Message level - Message
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
# Time formats
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

LXML = 'lxml'
# Pattern for finding strings like "Python 3.93 (security-fixes)"
PYTHON_VERSION_STATUS = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
# Pattern for finding a pdf file in a zip archive
PDF_ZIP_LINK = r'.+pdf-a4\.zip$'
