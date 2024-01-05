## This script imports the tinytweets.json file into your Cosmos database
## It will work for any json file containing a single array of objects
## There's nothing specific to llamaindex going on here
## You can get your data into mongo any way you like.

json_file = 'tweets.json'

# Load environment variables from local .env file
from dotenv import load_dotenv
load_dotenv()

import os
import json
from pymongo.mongo_client import MongoClient

# Load the tweets from a local file
with open(json_file, 'r') as f:
    tweets = json.load(f)

# Create a new client and connect to the server
client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv("MONGODB_DATABASE")]
collection = db[os.getenv("MONGODB_COLLECTION")]

# Insert the tweets into mongo
collection.insert_many(tweets)
