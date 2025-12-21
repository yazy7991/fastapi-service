from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import ReqBody, PostResponse
from app.db import Post,create_db_and_tables, get_async_session
from app.images import imagekit
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager
import shutil
import os
import uuid
import tempfile

"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database and tables
    await create_db_and_tables()
    yield
    # Shutdown: any cleanup can be done here if necessary
""" 

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Starting app...")
        await create_db_and_tables()
        print("Database initialized.")
        yield
    except Exception as e:
        print("Error during startup:", e)
        raise
    finally:
        print("Shutting down app...")

app = FastAPI(lifespan=lifespan)# Initialize FastAPI app with lifespan context manager

# Endpoint to upload a file 
@app.post("/upload")
async def upload_file(
    caption: str = Form(""), # Caption via form data. The form data is one of the many ways of sending data to an endpoint.
    file: UploadFile = File(...), # File upload via form data. The file data is one of the many ways of sending data to an endpoint.
    session: AsyncSession = Depends(get_async_session) # Dependency injection to get the database session
):
    
    #Create a temporary file to store the uploaded file
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name
        
        
        # Upload file to ImageKit
        with open(temp_file_path, "rb") as f:
            upload_result = imagekit.files.upload(
                file=f,
                file_name=file.filename,
                folder="/uploads",
                tags=["backend-upload"]
            )


        # Create a new Post record in the database SQLite ORM 
        new_post = Post(
            caption=caption,
            url=upload_result.url,  # In a real app, you'd store the file and get its URL
            file_type="video" if file.filename.endswith(".mp4") else "image",  # Simplified file type determination
            file_name=upload_result.name,  # Use the name returned by ImageKit
        )
        
        session.add(new_post) # Add the new post to the session/database. The function add works like add in git where it stages the changes to be committed
        await session.commit() # Commit the transaction to save changes to the database
        await session.refresh(new_post) # Refresh the instance to get updated data from the database
        return new_post # Return the created post data
        
        

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path) # Clean up the temporary file
        file.file.close() # Close the uploaded file

    

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