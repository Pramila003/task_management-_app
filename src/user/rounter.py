from fastapi import APIRouter, Depends,BackgroundTasks, status,Request
from src.user import controller
from sqlalchemy.orm import Session
from src.user.dtos import UserSchema,ResponseSchema,LoginSchema
from src.utils.db import get_db

user_route = APIRouter(prefix="/user")


@user_route.post("/register",response_model=ResponseSchema,status_code=status.HTTP_201_CREATED)
async def register(body: UserSchema,bg_task:BackgroundTasks, db: Session=Depends(get_db)):
    return await controller.register(body,db,bg_task)

@user_route.post("/login",status_code=status.HTTP_200_OK)
def login(body: LoginSchema,db:Session=Depends(get_db)):
    return controller.login(body,db)

@user_route.get("/is_auth")
def is_auth(request:Request, db:Session=Depends(get_db)):
    return controller.is_authenticated(request, db)