from fastapi import APIRouter, Depends, HTTPException
from app.database import get_database
from bson import ObjectId
from app.models import UserCreate, User
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
router = APIRouter()
db = Depends(get_database)
# @router.get("/test")
# def read_root():
#     return {"message": "Welcome to the API!"}

# CRUD for User
@router.post("/users/", response_model=User)
async def create_user(user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    # user_dict = user.model_dump()
    # last_item = await db.items.find_one(sort=[("_id", -1)])  # Find the last item by _id
    # next_id = 1 if last_item is None else last_item["_id"] + 1
    # user_dict["_id"] = next_id  # Create an ObjectId 
    # result = await database.users.insert_one(user_dict)
    # user_dict["id"] = str(result.inserted_id)
    # return user_dict

    last_user = await db["users"].find_one(sort=[("_id", -1)])  
    next_id = 1 if last_user is None else last_user["_id"] + 1  # Increment the last ID

    # Convert Pydantic model to dictionary
    user_dict = user.model_dump()  # Use .dict() to convert Pydantic model to dict
    user_dict["_id"] = next_id  # Set the new _id
    
    # Insert the new item into MongoDB
    result = await db["users"].insert_one(user_dict)
    
    # Convert ObjectId to string and add to the dictionary
    user_dict["id"] = str(result.inserted_id)
    
    return user_dict

@router.get("/users/", response_model=List[User])
async def read_users(database=db):
    users = []
    async for user in database.users.find():
        user["id"] = str(user["_id"])
        users.append(user)
    return users

@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: str, database=db):
    user = await database.users.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user["id"] = str(user["_id"])
    return user

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: UserCreate, database=db):
    updated_user = await database.users.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": user.model_dump()},
        return_document=True
    )
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user["id"] = str(updated_user["_id"])
    return updated_user

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: str, database=db):
    result = await database.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
