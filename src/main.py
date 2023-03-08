import logging
import re

from bs4 import BeautifulSoup
from requests_cache import CachedSession
from tqdm import tqdm
from urllib.parse import urljoin

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, EXPECTED_STATUS, LXML, MAIN_DOC_URL,
                       PDF_ZIP_LINK, PEP_DOC_URL, PYTHON_VERSION_STATUS)
from enums.headers import Header
from exceptions import FindVersionsException
from outputs import control_output
from utils import find_tag, get_response, is_none, mkdir_and_path


def whats_new(session: CachedSession) -> list[tuple[str, str, str]]:
    """Collects links to articles about innovations in Python
    and information about the authors and editors of articles."""
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = is_none(get_response(session, whats_new_url))
    results = [Header.first_row, ]  # Set the list where we will save the data
    soup = BeautifulSoup(response.text, LXML)
    main_div = find_tag(soup, 'div', {'class': 'toctree-wrapper'})
    li_tags = main_div.find_all('li', class_='toctree-l1')
    for li in tqdm(li_tags):
        # The first tag <a> has the hyper reference we are looking for
        tag_a = find_tag(li, 'a')
        href = tag_a.get('href')
        url = urljoin(whats_new_url, href)
        # Collecting information from the desired page
        response = is_none(get_response(session, url))
        soup = BeautifulSoup(response.text, LXML)
        python_version = find_tag(soup, 'h1').text
        editors = find_tag(soup, 'dl').text.replace('\n', ' ')
        results.append((url, python_version, editors))
    return results


def latest_versions(session: CachedSession) -> list[tuple[str, str, str]]:
    """Gathers information about Python version statuses."""
    response = is_none(get_response(session, MAIN_DOC_URL))
    results = [Header.first_row, ]  # Set the list where we will save the data
    soup = BeautifulSoup(response.text, LXML)
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' not in ul.text and ul == ul_tags[-1]:
            raise FindVersionsException('Не найден список c версиями Python')
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            # If the required list is not found,
            # the program is interrupted and exception is raised
            break
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
    response = is_none(get_response(session, downloads_url))
    soup = BeautifulSoup(response.text, LXML)
    table_tag = find_tag(soup, 'table', attrs={'class': 'docutils'})
    # compile() takes a string and returns a regular expression object.
    regex = re.compile(PDF_ZIP_LINK)
    pdf_a4_tag = find_tag(table_tag, 'a', {'href': regex})
    pdf_a4_link = pdf_a4_tag.get('href')
    archive_url = urljoin(downloads_url, pdf_a4_link)
    # Filename formed from the last element of the "archive_url"
    filename = archive_url.split('/')[-1]
    archive_path = mkdir_and_path(BASE_DIR, 'downloads', filename)
    # Downloading archive
    response = is_none(get_response(session, archive_url))
    # Recording is done in binary mode ('wb')
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session: CachedSession) -> list[tuple[str, str]]:
    """Counts the number of all pep documents,
    matches tabular data with those on the page of the document,
    sums the number of documents for each category"""
    response = is_none(get_response(session, PEP_DOC_URL))
    # Set the variables where we will save the data
    results, status_sum, total = [Header.status_quantity, ], {}, 0

    soup = BeautifulSoup(response.text, LXML)
    section_tag = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    tbody_tag = find_tag(section_tag, 'tbody')
    tr_tags = tbody_tag.find_all('tr')
    for pep in tqdm(tr_tags):
        total += 1
        status_letter = pep.td.abbr.text[1:]        # Letter from the table
        href = find_tag(pep, 'a').get('href')
        url = urljoin(base=PEP_DOC_URL, url=href)   # URL of pep document
        # Jumping to the document page
        response = is_none(get_response(session, url))
        soup = BeautifulSoup(markup=response.text, features=LXML)
        section_tag = find_tag(soup, 'section', attrs={'id': 'pep-content'})
        status = find_tag(section_tag, 'abbr').text  # Status from the page
        if status not in EXPECTED_STATUS[status_letter]:
            logging.info(
                f'\n'
                f'Несовпадающие статусы: \n'
                f'{url}\n'
                f'Статус в карточке: {status}\n'
                f'Ожидаемые статусы: {EXPECTED_STATUS[status_letter]}'
            )
        if status not in status_sum:
            status_sum[status] = 1
        else:
            # Sums the number of documents for each category
            status_sum[status] += 1
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
    configure_logging()
    logging.info('Парсер запущен!')
    # Passing valid choices to the parser of CLI arguments
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    # Reading arguments from the command line
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = CachedSession()
    if args.clear_cache:
        session.cache.clear()
    # Get the parser mode from the command line arguments
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
