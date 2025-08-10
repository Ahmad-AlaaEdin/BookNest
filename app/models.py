from pydantic import Field,BaseModel

class User(BaseModel):
    username:str = Field(...,min_length=3,max_length=15)
    password:str = Field(...,min_length=8,max_length=15)