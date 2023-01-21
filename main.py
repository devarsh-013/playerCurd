from fastapi import FastAPI
import models
from database import engine
from routers import api
# creates the db 
models.Base.metadata.create_all(bind= engine)

app = FastAPI(
    title='player_curd')

#includes file from the router
app.include_router(api.router)








