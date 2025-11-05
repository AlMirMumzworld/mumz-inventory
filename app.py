from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.config.settings import get_settings
from src.config.database import init_db
from src.apis import routes


logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Connect to the database before the application starts up"""

    init_db()
    logger.info('Successfully connected to the database!')

    yield

app = FastAPI(title=settings.TITLE,
              description=settings.DESCRIPTION,
              lifespan=lifespan,
              docs_url='/api')

app.include_router(routes)

app.mount("/static", StaticFiles(directory="src/static"), name="static")
app.mount("/", StaticFiles(directory="src/views", html=True), name="views")


if __name__ == "__main__":
    import uvicorn
    import argparse
    parser = argparse.ArgumentParser(description="Run the app")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--host", type=str, default="127.0.0.1")
    args = parser.parse_args()
    uvicorn.run(app="__main__:app",
                reload=True,
                port=args.port,
                host=args.host)
