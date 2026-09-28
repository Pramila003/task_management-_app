from pydantic import BaseModel

class TaskSchema(BaseModel):
    title : str | None = None
    description : str | None = None
    is_complete : bool  | None = None




class TaskResponseSchema(BaseModel):
    id: int
    title : str | None = None
    user_id : int 
    