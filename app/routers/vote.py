from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session

from .. import schemas,database,models,oauth2

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)

def vote(vote: schemas.Vote,
    db: Session = Depends(database.get_db), 
    current_user: int = Depends(oauth2.get_current_user)):
    #------
    #Checks if post when voting exists, if it does not, raise not found error.
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")
    #------
    #Checks to see if a vote from current user exists on the post
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    #------
    #If the action is to add a vote to a post, it will check if a vote is already there using vote_query.
    #If there, it exists, raise conflict, else add new vote
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}") 
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message" : "successfully added vote"}

    #-------
    #If 0 is inputted for dir, checks if post exists, if it is not found, raise 404
    #else it will delete vote.
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message" : "successfully deleted vote"}

