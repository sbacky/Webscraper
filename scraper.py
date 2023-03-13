from googlesearch import search
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup, ResultSet
import argparse
from collections import Counter
import sys

from exceptions import NoQueryException, InvalidSearchType


def run_argparse() -> argparse.ArgumentParser:
    """Returns parsed arguments passed in from the command line.

    Returns:
        argparse.ArgumentParser: Argument parser for parsing command line arguments in python
    """
    # Create ArgumentParser instance
    arg_parser = argparse.ArgumentParser(
        prog="Scraper",
        description="Takes a query or list of queries and returns the most common words found from the top 5 results of the query/queries",
        epilog="If query and multi-query options are set at the same time, then only the query option will be parsed and used."
    )
    # Add arguments
    arg_parser.add_argument("-q", "--query", type=str, help="Query string to google search. Use -m or --multi-query to provide a comma separated list of queries.")
    arg_parser.add_argument("-m", "--multi-query", type=str, help="Comma separated list of queries as a string.")
    arg_parser.add_argument("-n", "--num-results", type=int, help="Set the number of result pages to process for each query. Default is 5.")
    arg_parser.add_argument("-s", "--search", type=str, help="Specify to retrieve index of words from body text or meta tags")
    
    return arg_parser

def get_urls(query: str, num_results: int) -> list[str]:
    """Google search query and return top 5 resulting URLs as a list of strings. Uses googlesearch.search()
    to search google and return a list of URLs

    Args:
        query (str): Query string to google search
        num_results (int): Number of resulting urls to return. Default is 5

    Returns:
        list[str]: List of top 5 results from google searching query
    """
    urls = search(query, num_results=num_results, lang="en")
    return list(urls)
    
def get_soup(url: str) -> BeautifulSoup:
    """Takes a url as a string and returns content of HTMl page as BeautiulSoup. Sets
    User-Agent: Mozilla/5.0 header and timeout=5.

    Args:
        url (str): URL to send GET request to using requests module. URL is a string

    Returns:
        BeautifulSoup: Returns content of page body at URL passed as a BeautifulSoup.
    """
    try:
        session = requests.Session()
        page = session.get(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0'
            },
            timeout=5
        )
    except RequestException as e:
        print(e)
    
    soup = BeautifulSoup(page.text, 'html5lib')
    page.close()
    return soup

def get_body(soup: BeautifulSoup) -> str:
    """Takes a BeautifulSoup object and returns body text of parsed page.

    Args:
        soup (BeautifulSoup): Parsed content of HTML page.

    Returns:
        str: content of body text of page as a string.
    """
    body = soup.find('body')
    return body.text

def get_meta(soup: BeautifulSoup) -> ResultSet:
    """Takes a BeautifulSoup object and returns ResultSet of meta tags from parsed page.

    Args:
        soup (BeautifulSoup): Parsed content of HTMl page

    Returns:
        ResultSet: List wrapper for list of meta tags List[str]
    """
    meta = soup.find_all('meta')
    return meta

def processor(content: str) -> Counter[str]:
    """Index and keep count of each word in content passed as string and return as a dictionary 

    Args:
        content (str): String content of web page but can be used with any string based content. Splits
        string based on whitespace, strips away any remaining whitespace and deletes empty strings.

    Returns:
        dict[str, int]: an index of every word in content and a count of how many times that word
        appeared. Does not differentiate on case of word. For example, "word" and "Word" would be
        considered the same. 
    """
    common_words = ['a', 'the', 'at', 'for', 'we', 'on', 'us', 'our', 'with', 'and', 'to', '5px', 'of', 'or', 'if', 'in', 'var', 'none;', '0s,', '1px', '2px', '3', '3px', '0.5s', 'you', '3px', 'your', 'can', 'src', '0px', '2']
    common_symbols = ['&', '@', '!', '=', '}', '{', '0', '/', ')', '(', '-', '+', '=', '<', '>', '1', ':', '*', '#', '@', ';', '–']
    words = Counter(content.lower().split())
    for word in set(common_words):
        del words[word]

    keys = words.keys()
    for word in list(keys):
        for symbol in set(common_symbols):
            if symbol in word:
                del words[word]
                break
            
    return words

def body_main(queries: list[str], num_results: int) -> None:
    # Initiate variables
    word_count: Counter[str] = Counter()
    urls: list[str] = []
    # Get list of urls per search query
    for query in queries:
        urls += get_urls(query, num_results)
    # Get rid of duplicate URLs
    url_set = set(urls)
    # Process content from each url
    for url in url_set:
        # Get content from body of html page and return as a string
        soup = get_soup(url)
        content = get_body(soup)
        # Index each word and count how many times it appears
        words = processor(content)
        word_count.update(words)
    # Sort words by words appearing most to words appearing least
    print(word_count.most_common(20))
    
def meta_main(queries: list[str], num_results: int) -> None:
    urls: list[str] = []
    # Get list of urls per search query
    for query in queries:
        urls += get_urls(query, num_results)
    # Get rid of duplicate URLs
    url_set = set(urls)
    # Process content from each url
    for url in url_set:
        print(url)
        # Get content from body of html page and return as a string
        soup = get_soup(url)
        meta_tags = get_meta(soup)
        for tag in meta_tags:
            print(tag)
        print()

def main(queries: list[str], num_results: int, search_type: str) -> None:
    try:
        match search_type:
            case "":
                body_main(queries, num_results)
            case "b" | "body":
                body_main(queries, num_results)
            case "m" | "meta":
                meta_main(queries, num_results)
            case "a" | "all":
                body_main(queries, num_results)
                meta_main(queries, num_results)
            case _:
                raise InvalidSearchType(f'{search_type} is not a valid search type. Use "b", "m", "a", or leave blank')
    except InvalidSearchType as e:
        print(e)
        print(f'search_type: {search_type}')
        sys.exit(1)

if __name__ == "__main__":
    arg_parser = run_argparse()
    # Run parser and place extracted data in argparse.Namespace
    args = arg_parser.parse_args()
    # Get query/queries
    query: list[str]
    try:
        if args.query:
            query = args.query.split(",")
        elif args.multi_query:
            query = args.multi_query.split(",")
        else:
            raise NoQueryException("No Query was provided. Provide a query using -q or --query and try again. Use -h to see help menu")
    except NoQueryException as e:
        print(e)
        print(args)
        sys.exit(1)
    # Get num_results
    num_results = 5
    if args.num_results:
        num_results = args.num_results
    # Get search
    search_type = "" 
    if args.search:
        search_type = args.search
    
    main(query, num_results, search_type)
    print(args)
    