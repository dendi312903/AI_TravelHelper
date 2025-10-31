from fastapi import FastAPI

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
]

@app.get("/places")
def place():
	return places
