from datetime import datetime
from models import PlayerModel
from fastapi import HTTPException, status
import routers.admin.v1.schemas as schemas
from sqlalchemy.orm import Session
from sqlalchemy import text
from libs.utils import now

# function which gets player by id
def get_player_by_id(db: Session, player_id: str):
    return (
        db.query(PlayerModel)
        .filter(PlayerModel.id == player_id, PlayerModel.is_deleted == False)
        .first()
    )


# function which creates a player and takes Player schema which takes first_name and last_name
def create_player(db: Session, player: schemas.Player):

    db_user = PlayerModel(
        id=player.id, first_name=player.first_name, last_name=player.last_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# gets all the player with skip and limit arg where default is 0 for skip and 10 for limit
def get_player(db: Session, skip: int = 0, limit: int = 10):
    return db.execute(
        text(
            "SELECT * FROM player WHERE is_deleted = false LIMIT :limit OFFSET :offset "
        ),
        {"limit": limit, "offset": skip},
    ).fetchall()


# deletes player from the id
def delete_player(db: Session, player_id: str):
    db_player = get_player_by_id(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="player not found."
        )

    db_player.is_deleted = True

    db.commit()
    return


# updates player from the player id
def update_player(db: Session, player_id: str, player: schemas.PlayerUpdate):
    db_player = get_player_by_id(db=db, player_id=player_id)

    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="player not found."
        )

    db_player.first_name = player.first_name
    db_player.last_name = player.last_name
    db_player.updated_at = now()
    db.commit()
    db.refresh(db_player)
    return db_player
