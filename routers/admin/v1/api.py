from typing import List
from fastapi import APIRouter, Depends, Path, Header
import routers.admin.v1.schemas as schemas

from dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

import routers.admin.v1.crud.players as players



@router.post('/login', response_model=schemas.PlayerLoginResponse)

def login_player(
    player: schemas.PlayerLogin,
    db: Session = Depends(get_db)
):
    db_user = players.sign_in(db, player)
    return db_user
# A post request for creating a player
@router.post("/player")
def create_player(player: schemas.PlayerBase, db: Session = Depends(get_db)):


    return players.create_player(db=db, player=player)

#A get request for getting all the players with skip and limit arguments
@router.get("/player",response_model=List[schemas.PlayerShow])
def get_all_players(skip: int = 0, limit: int = 10, token:str = Header(None),db: Session = Depends(get_db)):


    players.verify_token(db=db,token=token)
    all_players = players.get_all_players(db=db, skip=skip, limit=limit)
    return all_players

#A get request to get a player by an id
@router.get("/player/{player_id}" ,response_model= schemas.PlayerShow)
def get_player_by_id(player_id:str = Path(default=None ,min_length=36,max_length=36),token:str = Header(None), db:Session = Depends(get_db)):
    players.verify_token(db=db,token=token)
    db_player = players.get_player(db=db,player_id=player_id)

    return db_player
#update function to update first_name and last_name
@router.put("/player/{player_id}")
def update_player(
    player: schemas.PlayerBase, db: Session = Depends(get_db),
    player_id: str = Path(default = None,min_length=36,max_length=36), 
    token:str = Header(None)
):
    players.verify_token(db=db,token=token)
    return players.update_player(db=db, player_id=player_id, player=player)

#A delete request for deleting a player from its id
@router.delete("/player/{player_id}")
def delete_player(player_id: str = Path(default = None, min_length=36, max_length=36), token:str = Header(None) ,db: Session = Depends(get_db)):
    players.verify_token(db=db,token=token)
    players.delete_player(db, player_id=player_id)
    return {"message:player has been deleted"}