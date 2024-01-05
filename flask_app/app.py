from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
from pymongo.mongo_client import MongoClient
from llama_index.vector_stores.azurecosmosmongo import AzureCosmosDBMongoDBVectorSearch
from llama_index.indices.vector_store.base import VectorStoreIndex

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Create a new client and connect to the server
client = MongoClient(os.getenv("MONGODB_URI"))

# connect to Atlas as a vector store
store = AzureCosmosDBMongoDBVectorSearch(
    client,
    db_name=os.getenv('MONGODB_DATABASE'), # this is the database where you stored your embeddings
    collection_name=os.getenv('MONGODB_VECTORS'), # this is where your embeddings were stored in 2_load_and_index.py
    index_name=os.getenv('MONGODB_VECTOR_INDEX') # this is the name of the index you created after loading your data
)
index = VectorStoreIndex.from_vector_store(store)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# This is just so you can easily tell the app is running
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/process_form', methods=['POST'])
@cross_origin()
def process_form():
    query = request.form.get('query')
    if query is not None:
        # query your data!
        # here we have customized the number of documents returned per query to 20, because tweets are really short
        query_engine = index.as_query_engine(similarity_top_k=20)
        response = query_engine.query(query)
        return jsonify({"response": str(response)})
    else:
        return jsonify({"error": "query field is missing"}), 400
