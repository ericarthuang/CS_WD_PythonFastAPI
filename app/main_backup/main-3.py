from operator import truediv
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, schemas, utils


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            port='5433',
            database='fastapi', 
            user='postgres', 
            password='Lawrence19981123',
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):

    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users", response_model=List[schemas.UserOut])
def get_users(db: Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.Useruser.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} does not exist"
        )

    return user


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI again"}

#@app.get("/posts")
#def get_posts():
#    cursor.execute("""SELECT * FROM posts""")
#    posts = cursor.fetchall()
#    return {"data": posts}

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)): 
    posts = db.query(models.Post).all()
    return posts

#@app.post("/posts", status_code = status.HTTP_201_CREATED)
#def create_post(post: Post): # Post is schema
#    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
#    new_post = cursor.fetchone()
#    conn.commit()
#    return {
#        "data": new_post,
#    }

@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,   db: Session=Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#@app.get("/posts/{id}")
#def get_post(id: int):
#    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id), ))
#    post = cursor.fetchone()
#    if not post:
#        raise HTTPException(
#            status_code=status.HTTP_404_NOT_FOUND,
#            detail=f"post with id: {id} was not found"
#        )
#    return {
#        "post_detail": post,
#    }

@app.get('/posts/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} was not found"
        )
    return post


#@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
#def delete_post(id: int):
#    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """ , (str(id),))
#    deleted_post = cursor.fetchone()
#    conn.commit()
#    if not deleted_post:
#        raise HTTPException(
#            status_code = status.HTTP_404_NOT_FOUND,
#            detail = f"post with id:{id} was not found",
#        )
#    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id:{id} was not found",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#@app.put("/posts/{id}")
#def update_post(id: int, post: Post):
#    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s where id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
#    update_post = cursor.fetchone()
#    conn.commit()
#    if update_post  == None :
#        raise HTTPException(
#            status_code = status.HTTP_404_NOT_FOUND,
#            detail = f"post with id:{id} was not found"
#        )
#    return {
#        "data": update_post,
#    }

@app.put('/posts/{id}', response_model=schemas.Post)
def update(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"post with id:{id} was not found"
    )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()








