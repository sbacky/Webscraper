# Webscraper

The purpuse of this project is to get a count of every word's occurance on a specified number of pages, determined by a google search. Arguments are passed from the command line. Plural and singular versions of words are treated as different words.

Current Version:

Displays counts of words in order from most occurrances to least occurances. Prints count of words to the console as a dictionary of tuples containing a string and an index.

| **options** | **help text** |
|---|---|
| -h, --help | show this help message and exit |
| -q QUERY, --query QUERY | Query string to google search. Use -m or --multi-query to provide a comma separated list of queries. |
| -m MULTI_QUERY, --multi-query MULTI_QUERY | Comma separated list of queries as a string. |
| -n NUM_RESULTS, --num-results NUM_RESULTS | Set the number of result pages to process for each query. Default is 5. |

## Content

* [Setup](#setup)
* [Methods](#methods)
* [Releases](#releases)

## Setup

>Assumes you already have python installed.

* Python
* Venv
* beautifulsoup4
* google

### **Venv**

>Venv is used for a python virtual environment and keeps each python projects dependancies separarte from each other. Venv comes prepackaged with the latest release of python.

run the following command to create a virtual environment with venv named .venv/

```console
python -m venv .venv
```

to activate newly created virtual environment, run the following command

```console
# For Mac/Linux
source .venv/bin/activate
# For Windows
.venv\Scripts\activate
```

### **Beautifulsoup4**

>Beautiful Soup is a Python library for pulling data out of HTML and XML files. It works with your favorite parser to provide idiomatic ways of navigating, searching, and modifying the parse tree.

Install beautifulsoup4 with pip by running the following command

```console
pip install beautifulsoup4
```

### **Google**

>Python bindings to the Google search engine

Install google package with pip by running the following command

```console
pip install google
```

## Methods

A list of URLs for each search query need to be collected. Each URL then needs to be visited and scraped for its text content. The text content gets processed and every word is indexed and counted. Words will be stripped and converted to lower case because we only care if it is the same word.

* get_urls()
* get_content()
* processor()
* main()

### **get_urls(query: str, num_results: int) -> list[str]**

>Google search query and return top 5 resulting URLs as a list of strings. Uses googlesearch.search() to search google and return a list of URLs

Args:

* query (str): Query string to google search
* num_results (int): Number of resulting urls to return. Default is 5

Returns:

* list[str]: List of top num_results from google by searching query

### **get_content(url: str) -> str**

>Takes a url as a string and returns body content of HTMl page as string. Sets User-Agent: Mozilla/5.0 header and timeout=5.

Args:

* url (str): URL to send GET request to using requests module. URL is a string

Returns:

* str: Returns content of page body at URL passed as a string.

### **processor(content: str) -> Counter[str]**

>Index and keep count of each word in content passed as string and return as a dictionary 

Args:
    
* content (str): String content of web page but can be used with any string based content. Splits string based on whitespace, strips away any remaining whitespace and deletes empty strings.

Returns:
    
* dict[str, int]: an index of every word in content and a count of how many times that word appeared. Does not differentiate on case of word. For example, "word" and "Word" would be considered the same.

## Releases

### Version 1.0.0

Displays counts of words in order from most occurrances to least occurances. Prints count of words to the console as a dictionary of tuples containing a string and an integer.

Uses Search() from googlesearch module to search google with a given query and return a list of URLs. The number of URLs returned is set via num_results parameter on the Search method. This can be set from the Command line by passing the -n or --num-results flag and then an integer greater than 0.

Uses requests module to perform GET requests to each URL in the list of URLs obtained from googlesearch.Search(). Then uses Beautifulsoup4 to parse the HTML and pull all text from the `<body>...</body>`.

Uses collections.Counter() to count each words occurance and place in a dictionary. Also used to modify dictionary by taking away common words and symbols that shouldnt be considered in the final result.

Uses argparse to implement command line arguments for easy CLI use. See table [here](#webscraper)
