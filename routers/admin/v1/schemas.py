from pydantic import BaseModel,Field

#player schema which will be used for creating players

class PlayerBase(BaseModel):

    
    first_name:str =  Field(min_length=3, max_length=40)
    last_name:str = Field(min_length=3, max_length=40)

#A schema which will be used to show players
class PlayerShow(BaseModel):

    first_name: str
    last_name: str

    class Config:

        orm_mode = True