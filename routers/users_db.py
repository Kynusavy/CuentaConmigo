from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_shema
from bson import ObjectId

router = APIRouter(prefix="/userdb", tags=["userdb"],
                responses={status.HTTP_404_NOT_FOUND : {"message": "No encontrado"}})

#creamos entidad user


#operacion lista de uduarios
@router.get("/",response_model=list[User])
async def users():
    return users_shema(db_client.users.find())

#operacion de un solo usuario por id a travez del path
@router.get("/{id}")
async def users(id: str):
    return search_user("_id", ObjectId(id))

#Operacion de consuta un solo usuraio por query
@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))

#Operacion creacion de un nuevo registro
@router.post("/",response_model=User,status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya exite")
    
    user_dict = dict(user)
    
    id = db_client.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.users.find_one({"_id" : id}))

    return User(**new_user)

#Operacion de edicion de un registro
@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        
        db_client.users.find_one_and_replace({"_id":ObjectId(user.id)}, user_dict)

    except:
        return {"error": "No se ha actualizado el usuario"} 
    
    return search_user("_id", ObjectId(user.id))


#operacion de vorrado deun resitro
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) #id por path
async def user(id: str):

    found = db_client.users.find_one_and_delete({"_id":ObjectId(id)})
  
    if not found:
        return {"error" : "No se ha eliminado el usuario"}

# def search_user(id: int):
#     users = filter(lambda user: user.id == id, users_list)
#     try:
#         return list(users)[0]
#     except:
#         return {"error": "No se ha enconntrado el usuario"}

#funcion auilial de busqueda generica por alguno de los campos de 
def search_user(field: str, key):
    
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha enconntrado el usuario"}