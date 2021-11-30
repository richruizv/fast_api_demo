#Python
from typing import Optional
from fastapi.datastructures import Default
from enum import Enum
#Pydantic
from pydantic import BaseModel, Field

#FastApi
from fastapi import FastAPI
from fastapi import Body,Query,Path

app = FastAPI()

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    yellow = "yellow"
    nohair = "no hair"

class Person(BaseModel):
    first_name: str = Field(..., min_length=1,max_length=50)
    last_name: str = Field(..., min_length=1,max_length=50)
    age: int = Field(..., gt=0,le=115)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)


@app.get("/")
def home():
    return {"Hello" : "World"}


# Request and Response Body
@app.post("/person/new")
def create_person(person: Person = Body(...)): # acces to the parameters of person

    return person

#Validations: query parameters   
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50, 
        title="person name",
        description="this is the person name, it's between 1 and 50 characters"
        ),
    age: Optional[str] = Query(
        ...,
        title="person age",
        description="This is the person age, it's required and must be greater than zero"
        ),
    email: Optional[str] = Query(None,regex=r"\w*@\w*")
):
    return {name : age}

#Validations: path parameters   
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(..., gt = 0)
):
    return {person_id : "it_exist"}


@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="person id",
        description="this is the person id",
        gt=0
    ),
    person: Person = Body(...)
):
    return {person_id : person }