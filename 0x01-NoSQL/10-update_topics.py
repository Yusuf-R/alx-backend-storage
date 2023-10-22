#!/usr/bin/env python3
""" Update School """
from typing import List


def update_topics(mongo_collection, name: str, topics: List[str]):
    """
    Update topics of a school document based on the name.

    Args:
      mongo_collection: A MongoDB collection object.
      name (string) will be the school name to update
      topics (list of strings) will be the list of topics
      approached in the school

    Returns:
      None

    Raises:
      None.
    """
    search: dict = {"name": name}
    update: dict = {"$set": {"topics": topics}}
    mongo_collection.update_many(search, update)
    return
