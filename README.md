# Image Upload service

## ⚠ Development Notes & Troubleshooting
### Virtual Environment Activation (Windows)

#### Issue
While setting up the project, the Python virtual environment (venv) could not be activated when using the default Command Prompt shell. As a result, required dependencies (e.g., fastapi, uvicorn) were not available when running the application.

#### Cause
The activation command for a Python virtual environment depends on the shell being used. An incompatible shell or incorrect activation command will prevent the environment from activating correctly.

#### Solution
Switch to the appropriate shell environment and use the corresponding activation command:

- Command Prompt: `venv\Scripts\activate`


- Powershell: `.\venv\Scripts\Activate.ps1`

- GitBash/WSL: `source venv/Scripts/activate`

After activating the virtual environment correctly, all dependencies were resolved and the application ran as expected.

## FastAPI Lifespan Causing Uvicorn to Exit
When using a custom `lifespan` context manager in FastAPI like this:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database and tables
    await create_db_and_tables()
    yield
    # Shutdown: any cleanup can be done here if necessary  


app = FastAPI(lifespan=lifespan)# Initialize FastAPI app with lifespan context manager
```
and running the app with: `uvicorn app.app:app --reload`, the server starts but immediately shuts down, and the reload functionality does not work.

### cause

The lifespan function completes immediately after yield, so Uvicorn thinks the app finished and exits.

### solution

There are two ways to fix this:
- Proper asynccontextmanager with shutdown handling

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    await create_db_and_tables()
    print("Database initialized. App is starting...")
    try:
        yield  # Keep app running while serving requests
    finally:
        # Optional cleanup on shutdown
        print("App is shutting down...")

app = FastAPI(lifespan=lifespan)
```
- Use FastAPI startup events (simpler)

```python
from fastapi import FastAPI
from app.db import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
async def startup():
    await create_db_and_tables()
    print("Database initialized.")
```

## 🌐 Networking Note: 0.0.0.0 vs 127.0.0.1

When running the FastAPI application with Uvicorn, the host parameter determines how the server is exposed:

- 127.0.0.1 (localhost)

    - Binds the server to the local loopback interface

    - Accessible only from the same machine

    - Recommended for standard local development

    - Does not typically trigger firewall warnings

- 0.0.0.0 (all interfaces)

    - Binds the server to all network interfaces on the machine (Wi-Fi, Ethernet, virtual adapters)

    - Allows access from other devices on the same local network (subject to firewall rules)

    - Commonly used for Docker, virtual machines, or LAN testing

    - May trigger operating system firewall prompts

### Note:
Binding to 0.0.0.0 does not automatically expose the application to the public internet. External access is still controlled by firewall settings and network configuration.