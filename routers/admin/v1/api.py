from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Response
import schemas

from dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api")

import routers.service as service

# A post request for creating a player
@router.post("/player/")
def create_player(player: schemas.Player, db: Session = Depends(get_db)):
    db_player = service.get_player_by_id(db=db, player_id=player.id)
    if db_player:
        raise HTTPException(status_code=400, detail="player already exist")

    return service.create_player(db=db, player=player)

#A get request for getting all the players with skip and limit arguments
@router.get("/player/")
def read_player(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    player = service.get_player(db=db, skip=skip, limit=limit)
    return player

#A get request to get a player by an id
@router.get("/player/{player_id}")
def get_player_by_id(player_id:str, db:Session = Depends(get_db)):
    db_player = service.get_player_by_id(db=db,player_id=player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="player not found."
        )

    return db_player


#A delete request for deleting a player from its id
@router.delete("/player/{player_id}")
def delete_player(player_id: str, db: Session = Depends(get_db)):

    service.delete_player(db, player_id=player_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/player/{player_id}")
def update_player(
    player_id: str, player: schemas.PlayerUpdate, db: Session = Depends(get_db)
):

    return service.update_player(db=db, player_id=player_id, player=player)
