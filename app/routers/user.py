from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
from ..import models,schemas,utils
from..database import get_db

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):

    #hash password
    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass

    new_user = models.User(**user.dict()) #** = kwargs to unpack dictionary
    db.add(new_user) # creates new post
    db.commit() # adds it to database
    db.refresh(new_user) # retrieve post created and stores in new_post
    return new_user

@router.get('/{id}', response_model = schemas.UserOut)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail = f"User with ID: {id} does not exist!")

    return user