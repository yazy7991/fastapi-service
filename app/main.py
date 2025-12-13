from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FastAPI Service",
    description="Backend API built with FastAPI",
    version="1.0.0",
)

# CORS configuration (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "success",
        "service": "fastapi-service",
        "version": "1.0.0",
    }
