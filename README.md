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


#### Author
Karapetian Zorik   
Russian Federation, St. Petersburg, Kupchino.