from app.models import Todo, TodoCreate
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_database
from datetime import datetime
from typing import List

router = APIRouter()
db = Depends(get_database)


@router.post("/todos/", response_model=Todo)
async def create_todo(todo: TodoCreate, database=db):
    todo_dict = todo.model_dump()
    todo_dict["_id"] = ObjectId()
    todo_dict["created_at"] = datetime.now()
    result = await database.todos.insert_one(todo_dict)
    todo_dict["id"] = str(result.inserted_id)
    return todo_dict

@router.get("/todos/", response_model=List[Todo])
async def read_todos(database=db):
    todos = []
    async for todo in database.todos.find():
        todo["id"] = str(todo["_id"])
        todos.append(todo)
    return todos

@router.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: str, database=db):
    todo = await database.todos.find_one({"_id": ObjectId(todo_id)})
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo["id"] = str(todo["_id"])
    return todo

@router.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, todo: TodoCreate, database=db):
    updated_todo = await database.todos.find_one_and_update(
        {"_id": ObjectId(todo_id)},
        {"$set": todo.model_dump()},
        return_document=True
    )
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    updated_todo["id"] = str(updated_todo["_id"])
    return updated_todo

@router.delete("/todos/{todo_id}", response_model=dict)
async def delete_todo(todo_id: str, database=db):
    result = await database.todos.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"detail": "Todo deleted"}