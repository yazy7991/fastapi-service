from fastapi import FastAPI, HTTPException
from app.schemas import ReqBody, PostResponse
from app.db import Post,create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database and tables
    await create_db_and_tables()
    yield
    # Shutdown: any cleanup can be done here if necessary  


app = FastAPI(lifespan=lifespan)

# Create a python dictionary to store post
text_posts = {
    1: {
        "title": "Morning Motivation",
        "content": "Start your day with purpose and a positive mindset."
    },
    2: {
        "title": "Tech Tip",
        "content": "Always validate user input to prevent unexpected bugs."
    },
    3: {
        "title": "Daily Reminder",
        "content": "Consistency beats intensity when building long-term habits."
    },
    4: {
        "title": "Learning Curve",
        "content": "Mistakes are proof that you are learning something new."
    },
    5: {
        "title": "Focus Time",
        "content": "Eliminate distractions to get deep, meaningful work done."
    },
    6: {
        "title": "Healthy Living",
        "content": "Drink water regularly and take short breaks to recharge."
    },
    7: {
        "title": "Problem Solving",
        "content": "Break complex problems into smaller, manageable pieces."
    },
    8: {
        "title": "Creative Spark",
        "content": "Creativity grows when you give yourself permission to experiment."
    },
    9: {
        "title": "Career Advice",
        "content": "Learning never stops in a fast-changing professional world."
    },
    10: {
        "title": "Evening Reflection",
        "content": "Review your day and acknowledge even the smallest wins."
    }
}


# GET endpoint -> returns all posts
@app.get("/posts")
def get_all_post(limit: int = None):
    if limit:
        return dict(list(text_posts.items())[:limit])
    """
    Retrieve all posts.

    Returns:
        dict: Mapping of post IDs to post data stored in `text_posts`.
    """
    return text_posts

# GET endpoint -> returns a specific post by id
@app.get("/posts/{post_id}")
def get_post(post_id: int)->PostResponse:
    """
    Retrieve a specific post by its ID.

    Args:
        post_id (int): The ID of the post to retrieve.

    Returns:
        dict: The post data corresponding to the given post ID.

    Raises:
        HTTPException: If the post with the given ID does not exist.
    """
    post = text_posts.get(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# POST endpoint -> create a new post
@app.post("/posts")
def create_post(req_body: ReqBody)->PostResponse:
    """
    Create a new post with the given request body.

    Args:
        req_body (ReqBody): The request body containing title and content.

    Actions:
        Adds a new post to the `text_posts` dictionary with a unique post ID.

    Returns:
        dict: A success message indicating the post was created.
    """
    new_post_id = max(text_posts.keys()) + 1
    new_post = {"title": req_body.title, "content": req_body.content}
    text_posts[new_post_id] = new_post
    return new_post