from src.user.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException,status, Request, BackgroundTasks
from pwdlib import PasswordHash
import jwt
from src.utils.settings import settings
from datetime import datetime, timedelta
from src.utils.mail import send_mail

password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

async def register(body:UserSchema,db:Session,  bg_task: BackgroundTasks):
    # print(body)
    # no duplicate user name 
    # email validation 
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(400,detail="Username already exist..")

    is_user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user:
        raise HTTPException(400,detail="Email already exist")

    hash_password= get_password_hash(body.password)

    new_user = UserModel(
        name = body.name,
        username= body.username,
        hash_password = hash_password,
        email = body.email
        
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    ## Send email confirmation
    # res = await send_mail([new_user.email])
    bg_task.add_task(send_mail,[new_user.email])
    # print(res)


    return new_user

def login(body:LoginSchema, db:Session):
    # print(body)
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not  user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="wrong username")

    if not verify_password(body.password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="wrong password")

    exp_time = datetime.now() +timedelta(minutes=settings.EXP_TIME)
    token = jwt.encode({"_id": user.id,"exp":exp_time}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    
    return {"token":token}

#TOKEN SEND     
def is_authenticated(request: Request, db: Session):
    auth_header = request.headers.get("authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authorization header missing or invalid format (Expected 'Bearer <token>')")
    token = auth_header.split(" ")[1]

    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(data)
          
        User_id = data.get("_id")
        user = db.query(UserModel).filter(UserModel.id == User_id).first()
        return user     
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")