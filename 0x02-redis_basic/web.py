#!/usr/bin/env python3
import requests
import redis
from functools import wraps

redis_client = redis.Redis()


# In this tasks, we will implement a get_page function
#    (prototype: def get_page(url: str) -> str:).
#
# The core of the function is very simple. It uses the requests module
# to obtain the HTML content of a particular URL and returns it.
#
# Start in a new file named web.py and do not reuse the code written
# in exercise.py.
#
# Inside get_page track how many times a particular URL was accessed in the
# key "count:{url}" and cache the result with an expiration time of 10secs.
# Tip: Use http://slowwly.robertomurray.co.uk to simulate a slow response and
# test your caching.
#
# Bonus: implement this use case with decorators.


def cache_and_count(fucn):
    @wraps(fucn)
    def wrapper(url: str) -> str:
        """Get page from url"""

        # create cache and count keys
        cache_key = "cache:{}".format(url)
        count_key = "count:{}".format(url)

        # check if cached content exists
        # if cached_content := redis_client.get(cache_key):
        #   return cached_content
        cached_content = redis_client.get(cache_key)
        if cached_content:
            return cached_content.decode("utf-8")

        # get content from url
        response = requests.get(url)
        if response.status_code != 200:
            return None
        content = response.text

        # cache the content with expiration of 10secs
        redis_client.setex(cache_key, 10, content.encode("utf-8"))

        # increament the caache count=
        redis_client.incr(count_key)
        return content

    return wrapper


@cache_and_count
def get_page(url: str) -> str:
    """Get page from url"""
    response = requests.get(url)
    return response.text
