from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, oauth2, database, models
# SQL complicated query I have ever written
# select word_database.*, count(vote_database.word_id) from word_database left join vote_database on word_database.id = vote_database.word_id where word_database.id = 7 group by word_database.id ;
router = APIRouter(prefix="/vote", tags=["vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user_id)):

    check_is_word_exist_query=db.query(models.Word).filter(models.Word.id == vote.word_id).first()

    if not check_is_word_exist_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"word with id: {vote.word_id} does not exists :)")

    vote_query = db.query(models.Vote).filter(
        models.Vote.word_id == vote.word_id, models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"this word with id: {vote.word_id} was already vote by user with id: {current_user.id}")
        # if not found_vote:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                         detail=f"word with id: {vote.word_id} not found")

        new_vote = models.Vote(word_id=vote.word_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote was successfully added :)"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"word with id: {vote.word_id} not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote was successfully deleted :)"}
