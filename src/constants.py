from pathlib import Path


BASE_DIR = Path(__file__).parent
RESULTS_DIR = BASE_DIR / 'results'

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
