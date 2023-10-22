#!/usr/bin/env python3
""" Update School """
import pymongo


def update_topics(mongo_collection, name: str, topics: list[str]):
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
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
