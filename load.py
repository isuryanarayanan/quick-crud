"""
This load file loads the contents of the data/courses.json file into the mongodb database.
"""

import os
import json
from pymongo import MongoClient, ASCENDING, DESCENDING

mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
mongodb_db = os.getenv("MONGODB_DB", "fastapi")

client = MongoClient(mongodb_uri)
db = client[mongodb_db]
collection = db["courses"]

with open('courses.json') as f:
    data = json.load(f)

for course in data:
    if "name" in course and collection.find_one({"name": course["name"]}) is None:
        collection.update_one(
            {
                "name": course["name"]
            },
            {
                "$set": {
                    "name": course["name"],
                    "date": course["date"],
                    "description": course["description"],
                    "domain": course["domain"],
                    "chapters": [
                        {
                            "name":chapter["name"],
                            "text":chapter["text"],
                            "ratings":{
                                "positive":0,
                                "negative":0
                            }
                        } for chapter in course["chapters"]],
                    "rating": 0
                }
            },
            upsert=True
        )


collection.create_index([("name", ASCENDING)])
collection.create_index([("date", DESCENDING)])
collection.create_index([("rating", DESCENDING)])

client.close()
