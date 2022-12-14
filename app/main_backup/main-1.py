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
    post = post.dict()
    post['id'] = randrange(0, 1000000000000)
    my_posts.append(post)
    return {
        "data": post,
    }


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id:{id} was not found", 
        )
    return {
        "post_detail": post,
    }
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if not index:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id:{id} was not found",
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index  == None :
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id:{id} was not found"
        )
    post_dict = post.dict()
    post_dict['id'] = id # setup id
    my_posts[index] = post_dict
    return {
        "data": post_dict,
    }
