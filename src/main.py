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
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    if response is None:
        return
    # Создание "супа".
    soup = BeautifulSoup(response.text, features=LXML)
    # Нахождение нужных блоков в "супе".
    main_div = find_tag(
        soup=soup,
        tag='div',
        attrs={'class': 'toctree-wrapper'}
    )
    all_li = main_div.find_all('li', class_='toctree-l1')
    # Выводим все ссылки через цикл из списка all_li.
    results = [first_row, ]
    for li in tqdm(all_li):
        tag_a = find_tag(soup=li, tag='a')
        href = tag_a.get('href')
        url = urljoin(base=whats_new_url, url=href)
        # Загрузка всех страниц со статьями.
        response = get_response(session, url)
        if response is None:
            # Если ссылка не загрузится, программа перейдёт к следующей.
            continue
        soup = BeautifulSoup(response.text, features=LXML)
        python_version = find_tag(soup=soup, tag='h1').text
        editors = find_tag(soup=soup, tag='dl').text.replace('\n', ' ')
        results.append((url, python_version, editors))
    return results


def latest_versions(session: CachedSession) -> list[tuple[str, str, str]]:
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, LXML)
    sidebar = find_tag(
        soup=soup,
        tag='div',
        attrs={'class': 'sphinxsidebarwrapper'}
    )
    ul_tags = sidebar.find_all('ul')
    # Перебор в цикле всех найденных списков.
    for ul in ul_tags:
        # Проверка, есть ли искомый текст в содержимом тега.
        if 'All versions' in ul.text:
            # Если текст найден, ищутся все теги <a> в этом списке.
            a_tags = ul.find_all('a')
            break
    # Если нужный список не нашёлся,
    # вызывается исключение и выполнение программы прерывается.
    else:
        raise FindVersionsException('Не найден список c версиями Python')

    results = [first_row, ]
    # Шаблон для поиска версии и статуса:
    pattern = PYTHON_VERSION_STATUS
    # Цикл для перебора тегов <a>, полученных ранее.
    for a_tag in a_tags:
        link = a_tag.get('href')
        # Поиск паттерна в ссылке.
        text_match = re.search(pattern=pattern, string=a_tag.text)
        # Если строка соответствует паттерну,
        # переменным присываивается содержимое групп, начиная с первой.
        if text_match is not None:
            version, status = text_match.groups()
        # Если строка не соответствует паттерну,
        # первой переменной присваивается весь текст, второй — пустая строка.
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))
    return results


def download(session: CachedSession) -> None:
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, LXML)
    table_tag = find_tag(soup=soup, tag='table', attrs={'class': 'docutils'})
    # compile() принимает строку, а возвращает объект регулярного выражения.
    regex = re.compile(PDF_ZIP_LINK)
    pdf_a4_tag = find_tag(soup=table_tag, tag='a', attrs={'href': regex})
    pdf_a4_link = pdf_a4_tag.get('href')
    # Получаем полную ссылку с помощью функции urljoin.
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    # Путь до новой директории
    downloads_dir = BASE_DIR / 'downloads'
    # Создайте директорию.
    downloads_dir.mkdir(exist_ok=True)
    # Получите путь до архива, объединив имя файла с директорией.
    archive_path = downloads_dir / filename
    # Загрузка архива по ссылке через HTTP метод get()
    response = session.get(archive_url)
    # В бинарном режиме открывается файл на запись по указанному пути.
    with open(archive_path, 'wb') as file:
        # Полученный ответ записывается в файл.
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session: CachedSession) -> list[tuple[str, str]]:
    response = get_response(session, PEP_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, LXML)
    section_tag = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    tbody_tag = find_tag(section_tag, 'tbody')
    tr_tags = tbody_tag.find_all('tr')
    # Заголовок таблицы и словарь с количеством PEP
    results = [status_quantity, ]
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
