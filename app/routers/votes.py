from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, models, oath2
from sqlalchemy.orm import Session
from .. database import get_db


router = APIRouter(
    prefix="/vote",
    tags=['Vote / Like Post']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):

    # First check if the post actally exists before votting
    # If post exists thencontiue withvoting, of not stop here
    check_post = db.query(models.Post).filter(
        models.Post.id == vote.post_id).first()
    if not check_post:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "message": f"post with the id: {vote.post_id} was not found"})
    else:
        # Check if the vote already exists and also check if the vote belongs to the current users
        # This is basically checking if the users user has already liked/voted this post
        vote_query = db.query(models.Vote).filter(
            models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
        found_vote = vote_query.first()

        # Direction one for creating vote / like
        # If not 1 then its delete vote / like
        if vote.dir == 1:
            if found_vote:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"user {current_user.id} has already liked/voted on post {
                        vote.post_id}"
                )

            # if not found then like or vote on the post
            new_vote = models.Vote(post_id=vote.post_id,
                                   user_id=current_user.id)
            db.add(new_vote)
            db.commit()

            return {"message": "successfully added vote"}

        else:

            # Delete vote if found
            # if not found indicate
            if not found_vote:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exists")

            vote_query.delete(synchronize_session=False)
            db.commit()

            return {"message": "successfully deleted vote"}
