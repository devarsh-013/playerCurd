
from database import Base
from sqlalchemy import String,INTEGER,Column,DateTime,Boolean
from datetime import datetime

#making player table using orm 

class PlayerModel(Base):
    __tablename__ = 'player'

    id = Column(String(50), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(100))
    email = Column(String(50))
    password = Column(String(255))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
