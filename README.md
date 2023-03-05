# Python parsing project

### Description
This parser will help you keep up to date with the latest changes in Python versions!

The parser can perform four functions:
1. Collect links to articles about innovations in Python and collect information about the authors and editors of articles.
2. Gather information about Python version statuses.
3. Download archive with up-to-date documentation.
4. Count the number of all pep documents, match tabular data with those on the page of the document, sum the number of documents for each category


### Technology
- Python 3.9.6
- beautifulsoup4 4.9.3
- prettytable 2.1.0
- requests-cache 0.6.3


### Project run on local server
1. Install and activate the virtual environment:
```py -m venv venv```
```. venv/Scripts/activate```

2. Install dependencies from requirements.txt:
```pip install -r requirements.txt```

4. Open the parser documentation to display available modes:
```py src/main.py -h```


### Example

The output of the parser with command line interface arguments "latest-versions" and "-o pretty":

| Ссылка на статью                     | Заголовок    | Редактор, Aвтор |
|--------------------------------------|--------------|-----------------|
| https://docs.python.org/3.12/        | 3.12         | in development  |
| https://docs.python.org/3.11/        | 3.11         | stable          |
| https://docs.python.org/3.10/        | 3.10         | stable          |
| https://docs.python.org/3.9/         | 3.9          | security-fixes  |
| https://docs.python.org/3.8/         | 3.8          | security-fixes  |
| https://docs.python.org/3.7/         | 3.7          | security-fixes  |
| https://docs.python.org/3.6/         | 3.6          | EOL             |
| https://docs.python.org/3.5/         | 3.5          | EOL             |
| https://docs.python.org/2.7/         | 2.7          | EOL             |
| https://www.python.org/doc/versions/ | All versions |                 |


#### Author
Karapetian Zorik   
Russian Federation, St. Petersburg, Kupchino.