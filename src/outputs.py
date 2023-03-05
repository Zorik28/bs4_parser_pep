import csv
import datetime as dt
import logging

from argparse import Namespace
from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT


def control_output(results: list[tuple], cli_args: Namespace) -> None:
    output = cli_args.output
    if output == 'pretty':
        pretty_output(results)
    elif output == 'file':
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(results: list[tuple]) -> None:
    """Terminal output function."""
    for row in results:
        print(*row)


def pretty_output(results: list[tuple]) -> None:
    """Outputs data in PrettyTable format."""
    table = PrettyTable()
    table.field_names = results[0]  # Set the first element as the title
    table.align = 'l'               # Aligning the table to the left
    table.add_rows(results[1:])     # Adding rows left to the table
    print(table)


def file_output(results: list[tuple], cli_args: Namespace) -> None:
    """Outputs data in .csv format file."""
    # Create the folder "results" if not exists
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    # Get the parser mode from the command line arguments
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    # Save the current date in the specified format
    now_formatted = now.strftime(DATETIME_FORMAT)
    filename = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / filename
    # Writing data to a file using the context manager in write mode ('w')
    with open(file_path, 'w', encoding='utf-8') as file:
        # dialect='unix' format is to ensure that the data
        # is recorded in the same way on different OS
        writer = csv.writer(file, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами был сохранён: {file_path}')
