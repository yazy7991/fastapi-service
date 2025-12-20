from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import ReqBody, PostResponse
from app.db import Post,create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database and tables
    await create_db_and_tables()
    yield
    # Shutdown: any cleanup can be done here if necessary  


app = FastAPI(lifespan=lifespan)# Initialize FastAPI app with lifespan context manager

# Endpoint to upload a file
@app.post("/upload")
async def upload_file(
    caption: str = Form(""), # Caption via form data. The form data is one of the many ways of sending data to an endpoint.
    file: UploadFile = File(...), # File upload via form data. The file data is one of the many ways of sending data to an endpoint.
    session: AsyncSession = Depends(get_async_session) # Dependency injection to get the database session
):
    
    # Create a new Post record
    new_post = Post(
        caption=caption,
        url="dummy url",  # In a real app, you'd store the file and get its URL
        file_type="dummy_type",  # In a real app, you'd use the actual file type
        file_name="dummy_name",  # In a real app, you'd use the actual file name
    )
    
    session.add(new_post) # Add the new post to the session/database. The function add works like add in git where it stages the changes to be committed
    await session.commit() # Commit the transaction to save changes to the database
    await session.refresh(new_post) # Refresh the instance to get updated data from the database

    return new_post # Return the created post data


# Endpoint to get the feed of posts
@app.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).order_by(Post.created_at.desc())) # Query to select all posts ordered by creation date descending
    posts = [row[0] for row in result.all()] # Extract Post instances from the result

    posts_data = [] # List to hold the serialized post data

    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),  # Convert UUID to stringfor response
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat() # Convert datetime to ISO format string
            }
           
        )
    
    return {"posts": posts_data} # Return the list of posts