from pydantic import BaseModel

class OutputBaseModel(BaseModel):
    class Config:
        orm_mode = True