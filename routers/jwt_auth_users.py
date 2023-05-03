from fastapi import APIRouter,HTTPException,status,Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime,timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "1fe5ab5834a659eda4714c56600f881072cc0182b96629b441c79b67ccfc96bd"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool

class UserDB(User):
    password: str

users_db = {
    "jonavila":{
        "username": "jonavila",
        "full_name": "Jhon Avila",
        "email": "jonavi@ky.co",
        "disable": False,
        "password": "$2a$12$wanK942ytd/Xg8Ugz2NAvuMvtlFHfzb2pgkBSvvi1t8gFon/Mkvga"
    },
    "edilson":{
        "username": "edilson",
        "full_name": "Edilson Malagon",
        "email": "edimal@ky.co",
        "disable": True,
        "password": "$2a$12$2GlbmofwcmL0hFtPXKvNHu8rxiIFj0wo3PJEMpQy5ZDIKuIs0DDC."
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticacion invalidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    
    except JWTError:
        raise exception

    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user

# @router.get("/")
# async def inicio():
#     return {"mensaje": "Operacion inicio jwt"}

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    
    if not crypt.verify(form.password,user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="La contraseña no es correcta")
    
    acces_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION)
 
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {"sub":user.username,"exp":expire}

    return {"access_token": jwt.encode(access_token,SECRET,algorithm=ALGORITHM) ,"token_type":"bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user