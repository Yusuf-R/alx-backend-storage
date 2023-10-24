#!/usr/bin/env python3
"""
    String Redis
"""
import uuid
from typing import Union, Callable
from functools import wraps
import redis


def count_calls(method: Callable = None) -> Callable:
    """function Decorator count calls"""
    name = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper method"""
        self._redis.incr(name)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator call history"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wraper function"""
        input: str = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)

        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)

        return output

    return wrapper


def replay(func: Callable):
    """Replay function"""
    r = redis.Redis()
    func_name = func.__qualname__
    number_calls = r.get(func_name)

    try:
        number_calls = number_calls.decode("utf-8")
    except Exception:
        number_calls = 0

    print(f"{func_name} was called {number_calls} times:")

    ins = r.lrange(func_name + ":inputs", 0, -1)
    outs = r.lrange(func_name + ":outputs", 0, -1)

    for cin, cout in zip(ins, outs):
        try:
            cin = cin.decode("utf-8")
        except Exception:
            cin = ""
        try:
            cout = cout.decode("utf-8")
        except Exception:
            cout = ""

        print(f"{func_name}(*{cin}) -> {cout}")


class Cache:
    """Functionality Redis"""

    def __init__(self):
        """Constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the given data in the cache and
        returns a unique key that can be used to retrieve it later.

        Args:
          data: The data to be stored in the cache.
          It can be a string, bytes, int or float.

        Returns:
          A string representing the unique key that
          can be used to retrieve the stored data later.
        """
        key = uuid.uuid4().hex
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn=None):
        """
        Retrieve the value associated with the given key from Redis.
        Args:
            key (str): The key to retrieve the value for.
            fn (callable, optional):
                A function to apply to the value before returning it.
        Returns:
            The value associated with the key, or None if the key is not found.
            the function is applied to the value before returning it.
        """
        data = self._redis.get(key)
        if data and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieve the value of a string key from Redis.
        Args:
            key (str): The key to retrieve the value for.
        Returns:
            str: The value of the key, as a string.
            If the key does not exist, returns None.
        """
        try:
            data = self._redis.get(key, str)
            data = str(data.decode("utf-8"))
            return data
        except Exception:
            return None

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer value from Redis, given a key.
        Args:
            key (str): The key to retrieve the integer value for.
        Returns:
            int: The integer value associated with the given key,
            or 0 if the key is not found or the value is not an integer.
        """
        try:
            data = self._redis.get(key, int)
            data = int(data.decode("utf-8"))
            return data
        except Exception:
            return 0
