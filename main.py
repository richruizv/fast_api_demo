#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field
from pydantic.networks import EmailStr

#FastApi
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import Body,Query,Path,Form,Header,Cookie,File

app = FastAPI()

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    yellow = "yellow"
    nohair = "no hair"

class Person(BaseModel):
    first_name: str = Field(..., min_length=1,max_length=50)
    last_name: str = Field(..., min_length=1,max_length=50,)
    age: int = Field(..., gt=0,le=115)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    password: str = Field(...,min_length=8,max_length=100)

    class Config:
            schema_extra = {
                "example": {
                    "first_name": "Rodrigo",
                    "last_name": "Lopez",
                    "age": 30,
                    "hair_color": "black",
                    "is_married": False
                }
            }

class Login(BaseModel):
    username : str = Field( ... , max_length=20 , example ="rich")
    password : str



@app.get("/", status_code=status.HTTP_204_NO_CONTENT)
def home():
    return {"Hello" : "World"}


# Request and Response Body
@app.post(
    "/person/new", 
    response_model=Person,
    response_model_exclude={"password"},
    status_code=status.HTTP_201_CREATED,
    tags=["persons"],
    summary="Create person in the app"
    )
def create_person(person: Person = Body(...)): # acces to the parameters of person
    """
    # Create Person

    This path operation creates a person in the app and save the information in the database

    ### Parameters
        - Request body parameter: 
            - ** person : Person ** -> A person model with first name, last name, age, hair color and marital status
    ### Returns
    A person model with first name, last name, age, hair color and marital status
    """
    return person

#Validations: query parameters   
@app.get(
    "/person/detail",
    tags=["persons"])
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
@app.get(
    "/person/detail/{person_id}",
    tags=["persons"]
    )
def show_person(
    person_id: int = Path(..., gt = 0)
):
    persons = [1,2,3,4,5]

    if person_id not in persons:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="This person doesn't even exist!"
        )
    return {person_id : "it_exist"}


@app.put(
    "/person/{person_id}",
    tags=["persons"]
    )
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


#form request
@app.post(
    path = "/login/",
    response_model=Login,
    status_code=status.HTTP_200_OK,
    tags=["basic"]
    )
def login(
    username : str = Form(...),
    password : str = Form(...)
):
    return Login(username=username,password="updated pass")

#cookies and header parameters
@app.post(
    path = "/contact",
    status_code=status.HTTP_200_OK,
    tags=["contact"]
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    email:  EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads : Optional[str] = Cookie(default=None)
):

    return user_agent

@app.post(
    path = "/post-image",
    tags=["files"]
)
def upload_file(
    image : UploadFile = File(...)
):
    return {
        "Filename" : image.filename,
        "Format" : image.content_type,
        "Size(kb)" : round(len(image.file.read())/1024) #filesize from image object
    }