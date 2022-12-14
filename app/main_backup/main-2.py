from operator import truediv
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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


my_posts = [
    {
        "id": 1,
        "title": "title of post 1",
        "content": "content of post 1",
    },
    {
        "id": 2,
        "title": "title of post 2",
        "content": "content of post 2",
    },
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i



@app.get("/")
def root():
    return {"message": "Welcome to FastAPI again"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_post(post: Post): # Post is schema
    
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
        
    new_post = cursor.fetchone()

    conn.commit()

    return {
        "data": new_post,
    }


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id), ))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    return {
        "post_detail": post,
    }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """ , (str(id),))

    deleted_post = cursor.fetchone()

    conn.commit()

    if not deleted_post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id:{id} was not found",
        )
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s where id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))

    update_post = cursor.fetchone()

    conn.commit()

    if update_post  == None :
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id:{id} was not found"
        )
    
    return {
        "data": update_post,
    }
