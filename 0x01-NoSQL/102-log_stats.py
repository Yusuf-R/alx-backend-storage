#!/usr/bin/env python3
""" Log stats """
from pymongo import MongoClient

# Write a Python script that provides some
# stats about Nginx logs stored in MongoDB:

# Database: logs
# Collection: nginx
# Display (same as the example):
# first line: x logs where x is the number of documents in this collection
# second line: Methods:
# 5 lines with the number of documents with the
# method = ["GET", "POST", "PUT", "PATCH", "DELETE"] in this order
# (see example below - warning: it’s a tabulation before each line)
# one line with the number of documents with:
# method=GET
# path=/status
if __name__ == "__main__":
    """
    This script provides some statistics about Nginx logs stored in MongoDB.
    It connects to a MongoDB instance running on localhost:27017, and retrieves
    all documents from the "nginx" collection in the "logs" database.

    It then counts the number of documents with each
    HTTP method ("GET", "POST", "PUT", "PATCH", "DELETE"),
    and the number of documents with method="GET" and path="/status".

    The script prints the following information:
         - The total number of logs in the collection.
         - The number of logs for each HTTP method.
         - The number of logs with method="GET" and path="/status".
         - The top 10 present IPs in the collection nginx of the database logs
    """
    client = MongoClient("mongodb://127.0.0.1:27017")
    logs = client.logs.nginx
    data = list(logs.find())
    cnt = len(data)
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    counts = {}
    for method in methods:
        counts[method] = logs.count_documents({"method": method})
    status_count = logs.count_documents({"method": "GET", "path": "/status"})
    pipeline = [
        {
            "$group": {
                "_id": "$ip",
                "count": {"$sum": 1}
                }
        },
        {
            "$project": {
                "ip": "$_id",
                "count": 1,
                "_id": 0
                }
        },
        {
            "$sort": {
                "count": -1
                }
        },

        {
            "$limit": 10
        },
    ]

    result = logs.aggregate(pipeline)
    reordered_result = [
        {"ip": doc["ip"], "count": doc["count"]} for doc in result
    ]
    print(f"{cnt} logs")
    print("Methods:")
    for method, count in counts.items():
        print(f"    method {method}: {count}")
    print(f"{status_count} status check")
    print("IPs:")
    for i in reordered_result:
        print("    {}: {}".format(i["ip"], i["count"]))
