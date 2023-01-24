from pydantic import BaseModel,Field

#player schema which will be used for creating players

class PlayerBase(BaseModel):

    
    first_name:str =  Field(min_length=3, max_length=40)
    last_name:str = Field(min_length=3, max_length=40)
    email:str = Field(min_length= 3, max_length=40)
    password: str = Field(min_length=3, max_length=50)
    
    
class PlayerLogin(BaseModel):

    email: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=3, max_length=50)

#A schema which will be used to show players
class PlayerShow(BaseModel):

    first_name: str
    last_name: str
    email:str

    class Config:

        orm_mode = True


class PlayerLoginResponse(BaseModel):
    id: str = Field(min_length=36, max_length=36)
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    email:str
    token: str

    class Config:
        orm_mode = True