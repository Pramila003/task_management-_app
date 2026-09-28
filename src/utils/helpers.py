from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.utils.settings import settings
import jwt 
from jwt.exceptions import InvalidTokenError
from src.user.models import UserModel 
from src.utils.db import get_db


def is_authenticated(request: Request, db: Session= Depends(get_db)):
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
    