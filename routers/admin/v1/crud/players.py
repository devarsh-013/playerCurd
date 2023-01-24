from datetime import datetime
from models import PlayerModel
from fastapi import HTTPException, status
import routers.admin.v1.schemas as schemas
from sqlalchemy.orm import Session
from libs.utils import generate_id,now,object_as_dict
import bcrypt
from jwcrypto import (
    jwk,
    jwt
)
from config import config
import json
import traceback

def get_player_by_email(db: Session, email: str):
    return db.query(PlayerModel).filter(PlayerModel.email == email, PlayerModel.is_deleted == False).first()

# function which gets player by id
def get_player_by_id(db: Session, player_id: str):
    return (
        db.query(PlayerModel)
        .filter(PlayerModel.id == player_id, PlayerModel.is_deleted == False)
        .first()
    )

def get_token(player_id, email):
    claims = {
        'id': player_id,
        'email': email,
        'time': str(now())
    }

    # Create a signed token with the generated key
    key = jwk.JWK(**config['jwt_key'])
    Token = jwt.JWT(header={"alg": "HS256"}, claims=claims)
    Token.make_signed_token(key)

    # Further encrypt the token with the same key
    encrypted_token = jwt.JWT(
        header={'alg': 'A256KW', 'enc': 'A256CBC-HS512'}, claims=Token.serialize())
    encrypted_token.make_encrypted_token(key)
    token = encrypted_token.serialize()
    return token


def verify_token(db: Session, token: str):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Missing token')
    else:
        try:
            key = jwk.JWK(**config['jwt_key'])
            ET = jwt.JWT(key=key, jwt=token)
            ST = jwt.JWT(key=key, jwt=ET.claims)
            claims = ST.claims
            claims = json.loads(claims)
            print(claims)
            db_player = get_player_by_id(db, player_id=claims['id'])
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if db_player is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Player not found')
        elif db_player.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Player not found')
        return db_player

def _create_password(password):
    password = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password, salt)
    password = password.decode('utf-8')
    return password


# function which creates a player and takes Player schema which takes first_name and last_name
def create_player(db: Session, player: schemas.PlayerBase):

    player_id = generate_id()
    player = player.dict()

    email = player['email']
    db_player = get_player_by_email(db, email=email)
    password = player['password']

    if db_player:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Player already exist.')
    
    player['password'] = _create_password(password)
    db_player = PlayerModel(
        id=player_id, **player
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player.id




def sign_in(db: Session, player: schemas.PlayerLogin):
    db_player = get_player_by_email(db, email=player.email)
    if db_player is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif db_player.is_deleted:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    hashed = db_player.password
    hashed = bytes(hashed, 'utf-8')
    password = bytes(player.password, 'utf-8')
    if not bcrypt.checkpw(password, hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    player = object_as_dict(db_player)

    player['token'] = get_token(db_player.id, db_player.email)
    return player

# gets all the player with skip and limit arg where default is 0 for skip and 10 for limit
def get_all_players(db: Session, skip: int = 0, limit: int = 10):

    db_player = db.query(PlayerModel).filter(PlayerModel.is_deleted == False).order_by(PlayerModel.first_name.desc()).offset(skip).limit(limit).all()
    return db_player

def get_player(db:Session,player_id:str):
    db_player = get_player_by_id(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="player not found."
        )
    
    return db_player


 # updates player from the player id
def update_player(db: Session, player_id: str, player: schemas.PlayerBase):
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

# deletes player from the id
def delete_player(db: Session, player_id: str):
    db_player = get_player_by_id(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="player not found."
        )

    db_player.is_deleted = True
    db_player.updated_at = now()

    db.commit()
    return

