## mongo_compass with atlas
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
load_dotenv()

MONGODB_URL = f"mongodb+srv://{os.getenv('username')}:{os.getenv('password')}@{os.getenv('uri')}/"

def get_database():
    client = AsyncIOMotorClient(MONGODB_URL)
    return client.testdb





## mongodb in local

# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId
# from typing import List, Optional, Dict

# # MongoDB connection setup
# MONGODB_URL = "mongodb://localhost:27017"
# async def get_database():
#     client = AsyncIOMotorClient(MONGODB_URL)
#     return client.local_db

## mongodb in local not working for now because getting an error of dependancies of other package of mongodb.


import logging

