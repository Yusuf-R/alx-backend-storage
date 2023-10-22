#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """
import pymongo

# Write a Python function that returns
# the list of school having a specific topic:

# Prototype: def schools_by_topic(mongo_collection, topic):
# mongo_collection will be the pymongo collection object
# topic (string) will be topic searched


def schools_by_topic(mongo_collection, topic: str) -> list:
    """
    Returns the list of school having a specific topic.
    Args:
      mongo_collection: A MongoDB collection object.
      topic (string) will be topic searched
    Returns:
      None
    Raises:
      None.
    """
    obj = mongo_collection.find({"topics": topic})
    return list(obj)
