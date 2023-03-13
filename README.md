# Webscraper

The purpuse of this project is to get a count of every word's occurance on a specified number of pages, determined by a google search. Arguments are passed from the command line. Plural and singular versions of words are treated as different words.

Displays counts of words in order from most occurrances to least occurances. Prints count of words to the console as a dictionary of tuples containing a string and an index.

Current Version: [0.1.1](#version-011)

## Content

* [Command Line](#command-line)
* [Setup](#setup)
* [Methods](#methods)
* [Releases](#releases)
    * [0.1.0](#version-010)
    * [0.1.1](#version-011)

## Command Line

>Has a command line interface. Use below table for available flags and expected parameters

| **options** | **help text** |
|---|---|
| -h, --help | show this help message and exit |
| -q QUERY, --query QUERY | Query string to google search. Use -m or --multi-query to provide a comma separated list of queries. |
| -m MULTI_QUERY, --multi-query MULTI_QUERY | Comma separated list of queries as a string. |
| -n NUM_RESULTS, --num-results NUM_RESULTS | Set the number of result pages to process for each query. Default is 5. |
| -s SEARCH, --search SEARCH | String specifying search type. Can be "b", "m" or "a". Default is "b". |

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

* run_argparse()
* get_urls()
* get_soup()
* get_body()
* get_meta()
* processor()
* main()

### **run_argparse() -> argparse.ArgumentParser**

>Returns parsed arguments passed in from the command line.

Returns:
* argparse.ArgumentParser: Argument parser for parsing command line arguments in python

### **get_urls(query: str, num_results: int) -> list[str]**

>Google search query and return top 5 resulting URLs as a list of strings. Uses googlesearch.search() to search google and return a list of URLs

Args:

* query (str): Query string to google search
* num_results (int): Number of resulting urls to return. Default is 5

Returns:

* list[str]: List of top num_results from google by searching query

### **get_soup(url: str) -> BeautifulSoup**

>Takes a url as a string and returns body content of HTMl page as BeautifulSoup. Sets User-Agent: Mozilla/5.0 header and timeout=5.

Args:

* url (str): URL to send GET request to using requests module. URL is a string

Returns:

* BeautifulSoup: Returns content of page body at URL passed as a BeautifulSoup object.

### **get_body(soup: BeautifulSoup) -> str**

>Takes a BeautifulSoup object and returns body text of parsed page.

Args:
* soup (BeautifulSoup): Parsed content of HTML page.

Returns:
* str: contnet of body text of page as a string.

### **get_meta(soup: BeautifulSoup) -> ResultSet**

>Takes a BeautifulSoup object and returns ResultSet of meta tags from parsed page.

Args:
* soup (BeautifulSoup): Parsed content of HTMl page

Returns:
* ResultSet: List wrapper for list of meta tags List[str]

### **processor(content: str) -> Counter[str]**

>Index and keep count of each word in content passed as string and return as a dictionary 

Args:
    
* content (str): String content of web page but can be used with any string based content. Splits string based on whitespace, strips away any remaining whitespace and deletes empty strings.

Returns:
    
* dict[str, int]: an index of every word in content and a count of how many times that word appeared. Does not differentiate on case of word. For example, "word" and "Word" would be considered the same.

## Releases

### Version 0.1.0

Displays counts of words in order from most occurrances to least occurances. Prints count of words to the console as a dictionary of tuples containing a string and an integer.

Uses Search() from googlesearch module to search google with a given query and return a list of URLs. The number of URLs returned is set via num_results parameter on the Search method. This can be set from the Command line by passing the -n or --num-results flag and then an integer greater than 0.

Uses requests module to perform GET requests to each URL in the list of URLs obtained from googlesearch.Search(). Then uses Beautifulsoup4 to parse the HTML and pull all text from the `<body>...</body>`.

Uses collections.Counter() to count each words occurance and place in a dictionary. Also used to modify dictionary by taking away common words and symbols that shouldnt be considered in the final result.

Uses argparse to implement command line arguments for easy CLI use. See table [here](#webscraper)

### Version 0.1.1

Added search type to specify whether to search for meta tags or for body text. Default is to search for body text. This is set by the -s or --search flag followed by "b" or "body" for body text, "m" or "meta" for meta tags, or "a" or "all" for both body text and meta tags. Meta tags are returned below the url they are found at and printed in the console.

Added InvalidSearchType Exception raised if the search type is not a valid selection. Search type must be one of the selections described above otherwise this exception will be raised.

Refactored code to separate code handling body text from code handling meta tags. This can be further refactored to take out similar code for handling the urls.

Update main() to use match case for search type. This can match any number of search types and is easily extendible if more search types are added.

### Future Updates

Export results to a specified file instead of to the console. Can be an additional argument to output results to a specified file. Need to check if file path is valid and file and user have appropriate permissions.
