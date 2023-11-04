#!/usr/bin/env python3
""" Module for web counting """
import requests
from flask import abort
import redis
from typing import Callable
from functools import wraps

redis_client = redis.Redis()


def cache_and_count(func: Callable) -> Callable:
    """Cache and count decorator

    This decorator function caches the content of a webpage for 10 seconds
    and also keeps track of the number of times the page has been accessed.

    It uses Redis as the caching mechanism and the requests library
    to fetch the content of the webpage.

    Args:
        fucn (function): The function to be decorated.

    Returns:
        function: The decorated function.

    Raises:
        None
    """

    @wraps(func)
    def wrapper(url):
        """Get page from url

        - This function fetches the content of a webpage from the given url.
        - It first checks if the content is already cached in Redis.
        - If it is, it returns the cached content. If not, it fetches
            the content from the url using the requests library.
        - If the response status code is not 200, it returns None.
            If the content is fetched successfully, it caches the content
            in Redis with an expiration time of 10 seconds and
            also increments the count of the number of times the
            page has been accessed.

        Args:
            url (str): The url of the webpage to fetch.

        Returns:
            str: The content of the webpage.

        Raises:
            None
        """

        # create cache and count keys
        # cache_key: str = "cache:{}".format(url)
        # count_key: str = "count:{}".format(url)

        # icreament the count first, kinda crazy though
        redis_client.incr(f'count:{url}')

        # check if cached content exists
        cached_content = redis_client.get(f'cache:{url}')
        if cached_content:
            return cached_content.decode("utf-8")

        # get content from url
        html = func(url)
        # cache the content with expiration of 10secs
        redis_client.setex(f'cache:{url}', 10, html)
        return html

    return wrapper


@cache_and_count
def get_page(url: str) -> str:
    """Get page from url"""
    response = requests.get(url)
    if response.status_code != 200:
        abort(404)
    return response.text
