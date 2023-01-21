from typing import List
from fastapi import APIRouter, Depends, Path
import routers.admin.v1.schemas as schemas

from dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api")

import routers.admin.v1.crud.players as players

# A post request for creating a player
@router.post("/player")
def create_player(player: schemas.PlayerBase, db: Session = Depends(get_db)):


    return players.create_player(db=db, player=player)

#A get request for getting all the players with skip and limit arguments
@router.get("/player",response_model=List[schemas.PlayerShow])
def get_all_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_players = players.get_all_players(db=db, skip=skip, limit=limit)
    return all_players

#A get request to get a player by an id
@router.get("/player/{player_id}" ,response_model= schemas.PlayerShow)
def get_player_by_id(player_id:str = Path(default=None ,min_length=36,max_length=36), db:Session = Depends(get_db)):
    db_player = players.get_player(db=db,player_id=player_id)

    return db_player

@router.put("/player/{player_id}")
def update_player(
    player_id: str, player: schemas.PlayerBase, db: Session = Depends(get_db)
):

    return players.update_player(db=db, player_id=player_id, player=player)

#A delete request for deleting a player from its id
@router.delete("/player/{player_id}")
def delete_player(player_id: str, db: Session = Depends(get_db)):

    players.delete_player(db, player_id=player_id)
    return {"message:player has been deleted"}