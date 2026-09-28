from src.task.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.task.models import TaskModel
from fastapi import HTTPException
from src.user.models import UserModel



def create_task(body:TaskSchema, db: Session, user:UserModel):
    # print(body.model_dump())
    data = body.model_dump()
    new_task = TaskModel(title = data["title"], description = data["description"],is_complete = data["is_complete"],user_id = user.id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

    

def get_task(db: Session):
    task = db.query(TaskModel).all()
    return task


def get_one_task(task_id: int,db: Session):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404,detail={"error code":"invalid task id"})
    return one_task

def update_task(body: TaskSchema, task_id: int, db: Session):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404,detail={"erro code":"task id does not exist"})
    one_task.title = body.title
    one_task.description = body.description
    one_task.is_complete = body.is_complete

    db.add(one_task)
    db.commit()
    db.refresh(one_task)

    return{"status":"data updated ", "data":one_task}

def update_spec(body: TaskSchema,task_id: int,db: Session):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404,detail={"error code":"no id "})

    body =  body.model_dump(exclude_unset=True)
    for field, value in body.items():
        setattr(one_task,field,value)

    db.add(one_task)
    db.commit()
    db.refresh(one_task)

    return one_task

def delete_task(task_id: int, db: Session):
    one_task=db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404,detail={"error code":"no id"})

    db.delete(one_task)
    db.commit()

    return None 
