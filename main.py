from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

DATABASE_FILE = "data.json"


class Item(BaseModel):
    channel:str
    description: str = None



@app.get("/")
def index():
    return{"result":"Hello!👋"}

@app.get("/items/{item_id}")
async def get_item(item_id:int):
    items = read_items_from_db()
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code = 404,detail = "item not found")
    return{"item":items[item_id]}

@app.post("/items/")
async def store_item(item:Item):
    
    items = read_items_from_db()
    items.append(item.model_dump())
    store_item_to_db(items)
    return{"result":item.model_dump()}

def read_items_from_db():
    try:
        with open(DATABASE_FILE,'r') as file:
            items = json.load(file)
    except FileNotFoundError:
        items = []
        
    return items
         
def store_item_to_db(data):
    with open(DATABASE_FILE,'w') as file:
        json.dump(data, file, indent=2)