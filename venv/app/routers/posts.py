from fastapi import FastAPI, HTTPException, Response, status, Depends,APIRouter
from sqlalchemy.orm import Session
from typing import  List
from .. import models, schemas, Oauth2
from ..database import get_db
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



@router.get("/", response_model=List[schemas.Post])
def get_posts(db : Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM Posts """)
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=201, response_model= schemas.Post)
def create_posts(post : schemas.PostCreate,db : Session = Depends(get_db), current_user: int= Depends(Oauth2.get_current_user)):
    print(current_user.email)
    new_posts= models.Post(**post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s , %s,%s) returning * """,(post.title,post.content,post.published))
    #new_posts =cursor.fetchone()
    #conn.commit()
    return  new_posts

@router.get("/{id}", response_model=schemas.Post)
def get_post(id : int,db : Session = Depends(get_db), current_user: int= Depends(Oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    #cursor.execute(""" SELECT *  from posts where id = %s""",(str(id)))
    #post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id:{id} was not found")
    return  post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db : Session = Depends(get_db), current_user: int= Depends(Oauth2.get_current_user)):
    
   # cursor.execute(""" DELETE from posts where id = %s  returning * """, (str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit
    
    post = db.query(models.Post).filter(models.Post.id == id)
    if  post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "post not found")
    

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int ,updated_post : schemas.PostCreate,db : Session = Depends(get_db), user_id: int= Depends(Oauth2.get_current_user)):
   # cursor.execute(""" UPDATE posts set title = %s, content = %s, published = %s where id = %s returning *""",(post.title, post.content,post.published , str(id)))
    #updated_post =  cursor.fetchone()
    #conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return  post_query.first()