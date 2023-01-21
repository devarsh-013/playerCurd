from pydantic import BaseModel

#player schema which will be used for creating players

class Player(BaseModel):

    id: str
    first_name: str
    last_name:str

#A schema which will be used while updating players
class PlayerUpdate(BaseModel):

    first_name: str
    last_name: str