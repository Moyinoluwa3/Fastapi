from fastapi import FastAPI, HTTPException, Response, status, Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
router = APIRouter(
    prefix="/users",
    tags=['Users']
)



@router.post("/", status_code=201, response_model=schemas.UserOutput )
def create_user(user: schemas.UserCreate,db : Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user= models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',response_model=schemas.UserOutput)
def Get_user(id: int,db : Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist")

    return user