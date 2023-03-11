import csv
import datetime as dt
import logging

from argparse import Namespace

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT
from utils import mkdir_and_path


def control_output(results: list[tuple], cli_args: Namespace) -> None:
    """Sending parsing results to the selected output function."""
    modes = {
        'pretty': pretty_output,
        'file': file_output,
        None: default_output
    }
    modes[cli_args.output](results, cli_args)


def default_output(results: list[tuple], s=None) -> None:
    """Terminal output function."""
    for row in results:
        print(*row)


def pretty_output(results: list[tuple], s=None) -> None:
    """Outputs data in PrettyTable format."""
    table = PrettyTable()
    table.field_names = results[0]  # Set the first element as the title
    table.align = 'l'               # Aligning the table to the left
    table.add_rows(results[1:])     # Adding rows left to the table
    print(table)


def file_output(results: list[tuple], cli_args: Namespace) -> None:
    """Outputs data in .csv format file."""
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    # Save the current date in the specified format
    now_formatted = now.strftime(DATETIME_FORMAT)
    filename = f'{parser_mode}_{now_formatted}.csv'
    # Create the folder "results" if not exists
    file_path = mkdir_and_path(BASE_DIR, 'results', filename)
    # Writing data to a file using the context manager in write mode ('w')
    with open(file_path, 'w', encoding='utf-8') as file:
        # dialect='unix' format is to ensure that the data
        # is recorded in the same way on different OS
        writer = csv.writer(file, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами был сохранён: {file_path}')
