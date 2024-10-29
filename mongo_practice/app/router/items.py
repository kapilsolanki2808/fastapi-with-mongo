from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.models import Item
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_database
from datetime import datetime
from typing import List

router = APIRouter()
db = Depends(get_database)
@router.get("/get/items/", response_model=List[Item])
async def read_items(db: AsyncIOMotorDatabase = Depends(get_database)):
    items = []
    
    # Use async for to iterate over the cursor
    async for item in db["items"].find():
        # Convert item to dictionary, you may need to handle ObjectId conversion
        item_dict = item
        item_dict["_id"] = str(item_dict["_id"])  # Convert ObjectId to string if needed
        items.append(item_dict)
        
    return items
# @router.post("/items/", response_model=Item)
# async def create_item(item: Item, db: AsyncIOMotorClient = Depends(get_database)):
#     last_item = await db["items"].find_one(sort=[("_id", -1)])  # Find the last item by _id
#     next_id = 1 if last_item is None else last_item["_id"] + 1
#     item_dict = item.model_dump()  # Convert Pydantic model to dictionary
#     item_dict["_id"] = next_id  # Create a new ObjectId for the item
#     result = await db.items.insert_one(item_dict)  # Insert item into MongoDB
#     item_dict["id"] = str(result.inserted_id)  # Convert ObjectId to string and add to the dictionary
#     return item_dict  #

@router.post("/items/", response_model=Item)
async def create_item(item: Item, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Find the last item by _id
    last_item = await db["items"].find_one(sort=[("_id", -1)])  
    next_id = 1 if last_item is None else last_item["_id"] + 1  # Increment the last ID

    # Convert Pydantic model to dictionary
    item_dict = item.dict()  # Use .dict() to convert Pydantic model to dict
    item_dict["_id"] = next_id  # Set the new _id
    
    # Insert the new item into MongoDB
    result = await db["items"].insert_one(item_dict)
    
    # Convert ObjectId to string and add to the dictionary
    item_dict["id"] = str(result.inserted_id)
    
    return item_dict
@router.get("/pipeline")
async def pipeline(db: AsyncIOMotorClient = Depends(get_database)):
    user_id = 1  # Replace with a valid user ID from your users collection

    # Pipeline to join items with user details
    pipeline = [
        {
            "$lookup": {
                "from": "users",           # Collection to join
                "localField": "_id",       # Field from items
                "foreignField": "_id",     # Field from users
                "as": "user_details"       # Output array field
            }
        },
        {
            "$match": { 
                "user_details._id": user_id  # Filter for specific user
            }
        },
        {
            "$project": {
                "name": 1,
                "description": 1,
                "price": 1,
                "user_details.name": 1,
                "user_details.company_name": 1,
                "user_details.age":1
            }
        }
    ]

    # Execute the aggregation
    cursor = db["items"].aggregate(pipeline)

    # Convert cursor to list and return
    result = await cursor.to_list(length=None)  # Get all results

    return result  # Return results as JSON


# @router.get("/get/items/", response_model=List[Item])
# async def read_items(db=Depends(get_database)):
#     items = []
#     async for item in db.deals.find():
#         import pdb;pdb.set_trace()
#         item_dict = item  # Convert item to dictionary
#         item_dict = str(item_dict)  # Convert ObjectId to string
#         items.append(item_dict)
#         if len(items) == 4:
#             break
#     return items