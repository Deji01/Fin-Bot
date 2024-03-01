from dotenv import load_dotenv
import logging
import os

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.settings import init_settings
from app.api.routers.chat import chat_router

load_dotenv()

app = FastAPI()


@app.get("/", include_in_schema=False)
def index():
    """
    This function represents the index endpoint of the application.
    No parameters are passed to this function.
    It returns a RedirectResponse to the "/docs" endpoint.
    """
    return RedirectResponse("/docs")


init_settings()

environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set


if environment == "dev":
    logger = logging.getLogger("uvicorn")
    logger.warning("Running in development mode - allowing CORS for all origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(chat_router, prefix="/api/chat")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", reload=True)
