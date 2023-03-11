from googlesearch import search
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import argparse
from collections import Counter

from exceptions import NoQueryException


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
    
def get_content(url: str) -> str:
    """Takes a url as a string and returns body content of HTMl page as string. Sets
    User-Agent: Mozilla/5.0 header and timeout=5.

    Args:
        url (str): URL to send GET request to using requests module. URL is a string

    Returns:
        str: Returns content of page body at URL passed as a string.
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
    body = soup.find('body')
    return body.text

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
    common_words = ['a', 'the', 'at', 'for', 'with', 'and', 'to', 'of', 'or', 'if', 'in', 'var', 'none;', 'you', 'your', 'font-weight:', 'padding:', 'margin:', 'can', 'width:']
    common_symbols = ['&', '@', '!', '=', '\{\}', '}', '{', '//', '0;', '});', '0', '/', ')', '(', '-']
    words = Counter(content.lower().split())
    for word in set(common_words):
        del words[word]
    for symbol in set(common_symbols):
        del words[symbol]
    return words
    

def main(queries: list[str], num_results: int=5) -> None:
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
        content = get_content(url)
        # Index each word and count how many times it appears
        words = processor(content)
        word_count.update(words)
    # Sort words by words appearing most to words appearing least
    print(word_count.most_common(20))

if __name__ == "__main__":
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
        query = ['default']
            
    if args.num_results:
        main(query, args.num_results)
    else:
        main(query)
                
    print(args)
    