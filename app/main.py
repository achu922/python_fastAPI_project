
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


from.config import Settings
config_settings = Settings()
print(config_settings.database_username)

#models.Base.metadata.create_all(bind=engine) #found in fastAPI SQL relational Database

app = FastAPI()

origins = ["https://www.google.com", "https:://www.youtube.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Wiring up our routers : post,user,auth and vote
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)







