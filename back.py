from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

places = [
    {
    "id":1,
    "name":"Red Square",
    "adding data":"31.10.25"
    },
    {
    "id":2,
    "name":"Petrovkyy Park",
    "adding data":"31.10.25"
    },
    {
    "id":3,
    "name":"1231412",
    "adding data":"04.11.1941"
    },
]

@app.get("/places",
         tags=["Места"],
         summary="Получить все места")
def place():
    return places

@app.get(
    "/places/{place_id}",
         tags=["Места"],
         summary="Получить конкретное место")
def get_book(place_id: int):
    for place in places:
        if place["id"] == place_id:
            return place
    raise HTTPException(status_code=404, detail="Место не найдено")

class NewPlace(BaseModel):
    name: str
    adding_data: str

@app.post("/places", tags=["Места"])
def create_book(new_place: NewPlace):
    places.append({
        "id": len(places) + 1,
        "title": new_place.name,
        "author": new_place.adding_data,
    })
    return {"success": True}