from fastapi import FastAPI
from fastapi import HTTPException


app = FastAPI()

# Create a python dictionary to store post
text_posts ={"1": {"title": "First Post", "content": "This is the content of the first post."},
             "2": {"title": "Second Post", "content": "This is the content of the second post."}}

# GET endpoint -> returns all posts
@app.get("/posts")
def get_all_post():
    """
    Retrieve all posts.

    Returns:
        dict: Mapping of post IDs to post data stored in `text_posts`.
    """
    return text_posts

# GET endpoint -> returns a specific post by id
@app.get("/posts/{post_id}")
def get_post(post_id: str):
    """
    Retrieve a specific post by its ID.

    Args:
        post_id (str): The ID of the post to retrieve.

    Returns:
        dict: The post data corresponding to the given post ID.

    Raises:
        HTTPException: If the post with the given ID does not exist.
    """
    post = text_posts.get(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

