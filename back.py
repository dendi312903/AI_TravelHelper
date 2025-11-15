from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()
engine = create_async_engine('sqlite+aiosqlite:///database.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass

class PlaceModel(Base):
    __tablename__ = "places"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    adding_data: Mapped[str]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/setup_database')
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}

class PlaceAddSchema(BaseModel):
    name: str
    adding_data: str

class PlaceSchema(PlaceAddSchema):
    id: int


@app.get('/places')
async def get_places(session: SessionDep):
    query = select(PlaceModel)
    result = await session.execute(query)
    return result.scalars().all()


# @app.get(
#     "/places/{place_id}",
#          tags=["Места"],
#          summary="Получить конкретное место")
# def get_book(place_id: int):
#     for place in places:
#         if place["id"] == place_id:
#             return place
#     raise HTTPException(status_code=404, detail="Место не найдено")

class NewPlace(BaseModel):
    name: str
    adding_data: str

@app.post('/places')
async def add_places(data: PlaceAddSchema, session: SessionDep):
    new_place = PlaceModel(
        name=data.name,
        adding_data=data.adding_data
    )
    session.add(new_place)
    await session.commit()
    return {"ok": True}