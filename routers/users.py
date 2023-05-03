from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"message": "No encontrado"}})

#creamos entidad user

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id= 1, name="Jon",surname="Avila",url="https://jonavila.ia",age=41),
        User(id= 2, name="Jon1",surname="Avila1",url="https://jonavila.ia1",age=42),
        User(id= 3, name="Jon2",surname="Avila2",url="https://jonavila.ia",age=31)]

@router.get("/usersjson")
async def usersjason():
    return [{"name":"Brais", "surname": "moura", "url": "https://moure.dev", "age": 25},
            {"name":"Brais1", "surname": "moura1", "url": "https://moure.dev1"},
            {"name":"Brais2", "surname": "moura2", "url": "https://moure.dev2"}]


@router.get("/")
async def users():
    return users_list 

@router.post("/",status_code=201)
async def user(user: User):
    users_list.append(user)

@router.put("/user/")
async def user(user: User):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            return user

@router.delete("/user/{id}") #id por path
async def user(id: int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]  


