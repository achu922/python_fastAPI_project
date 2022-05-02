import random
from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional


from ..import models,schemas, oauth2
from..database import get_db

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

#**********GET ALL POSTS for LOGGED IN USER ID*********************
@router.get("/",response_model=List[schemas.PostOUT])
def get_posts(db:Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user), 
                limit:int = 10, skip:int = 0, search:Optional[str] = ""):
#%20 is space | EX: {{URL}}posts?search=gma
    print(limit)
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    
    return posts
#**********GET ALL POSTS for LOGGED IN USER ID*********************


#**********CREATE A POST*********************
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.get_current_user)): #makes user have to be signed in to do post

    #Do not use fstrings to pass data in directly, prevents SQL injection attacks. 
    # cursor.execute("""INSERT INTO public."Posts" (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published ))
    # new_post = cursor.fetchone() #Fetches the new post created

    # connection.commit() #Saves it into Postgres DATABASE
    
    # new_post = models.Post(
    #     title = post.title, content = post.content, published = post.published)
    
    new_post = models.Post(owner_id = current_user.id, **post.dict()) #** = kwargs to unpack dictionary
    db.add(new_post) # creates new post
    db.commit() # adds it to database
    db.refresh(new_post) # retrieve post created and stores in new_post
    return new_post 
#**********CREATE A POST*********************

#**********GET ALL POSTS*********************
@router.get("/public",response_model=List[schemas.Post])
def get_posts(db:Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    posts = db.query(models.Post).all()
    return posts
#**********GET ALL POSTS*********************

#**********GET A POST BY ID*********************
@router.get("/{id}" ,response_model=schemas.PostOUT)
def get_post(id: int, db:Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM public."Posts" WHERE id = %s RETURNING *""", (str(id),)) #Make sure to use comma
    # g_onepost = cursor.fetchone() # since there will always be a unqiue ID for each post

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
   
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"postID:{id} was not found")

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not Authorized to Perform action!")

    return post
#**********GET A POST BY ID*********************

#**********DELETE A POST BY ID*********************
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    #first find index in array with target ID
    # cursor.execute("""DELETE FROM public."Posts" WHERE id = %s RETURNING* """, (str(id),))
    # d_onepost = cursor.fetchone()
    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post of id: {id} was not found!")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not Authorized to Perform action!")
        
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
#**********DELETE A POST BY ID*********************

#**********UPDATE A POST BY ID*********************
@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, upd_post:schemas.PostCreate, db:Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE public."Posts" SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                                                 (post.title,post.content,post.published,str(id)))
    # u_post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    postFirst = post_query.first()

    if postFirst == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post of id: {id} was not found!")

    post_query.update(upd_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
#**********UPDATE A POST BY ID*********************