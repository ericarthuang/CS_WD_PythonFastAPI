import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    #print(res.json())
    #print(len(res.json()))
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client):
    res =  client.get('/posts/')
    print(res.json())
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client):
    res = authorized_client.get('/posts/88888')
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert  post.Post.id == test_posts[0].id


def test_unauthorized_user_delete_posts(client, test_posts):
    res = client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 204


def test_delete_post_not_exist(authorized_client):
    res = authorized_client.delete('/posts/88888')
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_posts):
    data = {
        "title": "update title",
        "content": "update content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)

    assert res.status_code == 200


def test_other_user_update_post(authorized_client, test_posts):
    data = {
        "title": "update title",
        "content": "update content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f'/posts/{test_posts[3].id}', json=data)

    assert res.status_code == 403


def test_unauthorized_user_update_posts(client, test_posts):
    res = client.put(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401


def test_update_post_not_exist(authorized_client, test_posts):
    data = {
    "title": "update title",
    "content": "update content",
    "id": test_posts[3].id
}
    res = authorized_client.put('/posts/88888', json=data)
    assert res.status_code == 404
