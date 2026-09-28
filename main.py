from fastapi import FastAPI
from src.utils.db import Base, engine
# from src.task.models import TaskModel
from src.task.router import task_routes
from src.user.rounter import user_route

Base.metadata.create_all(engine)    #whenever server start it will fisrt connect ot the database = get connected==> all table define in project will get created in database   ONLY ONE TIME EXCUTE JUST CHECK TABLE EXIST OR NOT ANOT USED TO ALTER 

app = FastAPI(title= "This is my management application") 
app.include_router(task_routes)
app.include_router(user_route)