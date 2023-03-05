import logging
import re

from bs4 import BeautifulSoup
from requests_cache import CachedSession
from tqdm import tqdm
from urllib.parse import urljoin

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, EXPECTED_STATUS, LXML, MAIN_DOC_URL,
                       PDF_ZIP_LINK, PEP_DOC_URL, PYTHON_VERSION_STATUS)
from enums.headers import first_row, status_quantity
from exceptions import FindVersionsException
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session: CachedSession) -> list[tuple[str, str, str]]:
    """Collects links to articles about innovations in Python
    and information about the authors and editors of articles."""
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    if response is None:
        return
    results = [first_row, ]  # Set the list where we will save the data
    soup = BeautifulSoup(response.text, LXML)
    main_div = find_tag(soup, 'div', {'class': 'toctree-wrapper'})
    li_tags = main_div.find_all('li', class_='toctree-l1')
    for li in tqdm(li_tags):
        # The first tag <a> has the hyper reference we are looking for
        tag_a = find_tag(li, 'a')
        href = tag_a.get('href')
        url = urljoin(whats_new_url, href)
        # Collecting information from the desired page
        response = get_response(session, url)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, LXML)
        python_version = find_tag(soup, 'h1').text
        editors = find_tag(soup, 'dl').text.replace('\n', ' ')
        results.append((url, python_version, editors))
    return results


def latest_versions(session: CachedSession) -> list[tuple[str, str, str]]:
    """Gathers information about Python version statuses."""
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    results = [first_row, ]  # Set the list where we will save the data
    soup = BeautifulSoup(response.text, LXML)
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            # If the required list is not found,
            # the program is interrupted and exception is raised
            break
    else:
        raise FindVersionsException('Не найден список c версиями Python')
    pattern = PYTHON_VERSION_STATUS
    for a_tag in a_tags:
        link = a_tag.get('href')
        # Search for pattern matching in the a_tag
        text_match = re.search(pattern=pattern, string=a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))
    return results


def download(session: CachedSession) -> None:
    """Downloads archive with up-to-date documentation."""
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, LXML)
    table_tag = find_tag(soup, 'table', attrs={'class': 'docutils'})
    # compile() takes a string and returns a regular expression object.
    regex = re.compile(PDF_ZIP_LINK)
    pdf_a4_tag = find_tag(table_tag, 'a', {'href': regex})
    pdf_a4_link = pdf_a4_tag.get('href')
    archive_url = urljoin(downloads_url, pdf_a4_link)
    # Filename formed from the last element of the "archive_url"
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    # Downloading archive
    response = get_response(session, archive_url)
    if response is None:
        return
    # Recording is done in binary mode ('wb')
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session: CachedSession) -> list[tuple[str, str]]:
    """Counts the number of all pep documents,
    matches tabular data with those on the page of the document,
    sums the number of documents for each category"""
    response = get_response(session, PEP_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, LXML)
    section_tag = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    tbody_tag = find_tag(section_tag, 'tbody')
    tr_tags = tbody_tag.find_all('tr')
    results = [status_quantity, ]  # Set the list where we will save the data
    status_sum = {}
    total = 0
    for pep in tqdm(tr_tags):
        total += 1
        # Извлекаем букву статуса
        status_letter = pep.td.abbr.text[1:]
        # Находим гиперссылку на страницу pep
        href = find_tag(pep, 'a').get('href')
        # Получаем ссылку на страницу pep
        url = urljoin(base=PEP_DOC_URL, url=href)
        # Извлекаем статус со страницы pep
        response = get_response(session, url)
        if response is None:
            continue
        soup = BeautifulSoup(markup=response.text, features=LXML)
        section_tag = find_tag(soup, 'section', attrs={'id': 'pep-content'})
        status = find_tag(section_tag, 'abbr').text
        if status not in EXPECTED_STATUS[status_letter]:
            logging.info(
                f'\n'
                f'Несовпадающие статусы: \n'
                f'{url}\n'
                f'Статус в карточке: {status}\n'
                f'Ожидаемые статусы: {EXPECTED_STATUS[status_letter]}'
            )
        # количество PEP в каждом статусе
        if status not in status_sum:
            status_sum[status] = 1
        else:
            status_sum[status] += 1
    # Отсортируем словарь и вернём список кортежей
    sorted_status_sum = sorted(status_sum.items())
    results.extend(sorted_status_sum)
    results.append(('Total', total))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main() -> None:
    # Запускаем функцию с конфигурацией логов.
    configure_logging()
    # Отмечаем в логах момент запуска программы.
    logging.info('Парсер запущен!')
    # Конфигурация парсера аргументов командной строки —
    # передача в функцию допустимых вариантов выбора.
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    # Считывание аргументов из командной строки.
    args = arg_parser.parse_args()
    # Логируем переданные аргументы командной строки.
    logging.info(f'Аргументы командной строки: {args}')
    # Загрузка веб-страницы с кешированием.
    session = CachedSession()
    # Получение из аргументов командной строки нужного режима работы.
    # Если был передан ключ '--clear-cache', то args.clear_cache == True.
    if args.clear_cache:
        # Очистка кеша.
        session.cache.clear()
    parser_mode = args.mode
    # Поиск и вызов нужной функции по ключу словаря.
    # С вызовом функции передаётся и сессия.
    results = MODE_TO_FUNCTION[parser_mode](session)

    # Если из функции вернулись какие-то результаты,
    if results is not None:
        # передаём их в функцию вывода вместе с аргументами командной строки.
        control_output(results, args)
    # Логируем завершение работы парсера.
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
