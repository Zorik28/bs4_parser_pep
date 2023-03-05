from pathlib import Path


BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_DOC_URL = 'https://peps.python.org/'

# Описание формата логов:
# Время записи – Уровень сообщения – Cообщение.
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
# Формат времени
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

# Перечень статусов и их буквенное обозначение
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
# Шаблон для нахождения строк типа "Python 3.93 (security-fixes)"
PYTHON_VERSION_STATUS = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
# Шаблон для нахождения файла формата pdf в zip архиве
PDF_ZIP_LINK = r'.+pdf-a4\.zip$'
