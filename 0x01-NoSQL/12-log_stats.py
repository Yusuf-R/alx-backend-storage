#!/usr/bin/env python3
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

client = MongoClient("mongodb://127.0.0.1:27017")
logs = client.logs.nginx
data = list(logs.find())
cnt = len(data)

methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
counts = {}

for method in methods:
    counts[method] = logs.count_documents({"method": method})

status_count = logs.count_documents({"method": "GET", "path": "/status"})

print(f"{cnt} logs")
print("Methods:")
for method, count in counts.items():
    print(f"    {method}: {count}")

print(f"{status_count} status check")
