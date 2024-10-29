from fastapi import FastAPI
from app.router import user, items, todo


app = FastAPI()



app.include_router(user.router, prefix="/user", tags=['user'])
app.include_router(items.router, prefix="/items", tags=['items'])
app.include_router(todo.router, prefix="/todo", tags=['todo'])




