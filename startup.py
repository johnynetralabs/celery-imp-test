from fastapi import FastAPI
from contextlib import asynccontextmanager
from core import settings, mongo_connector

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- STARTUP ----
    try:
        # MongoDB init
        await mongo_connector.initialize(
            mongo_url=settings.MONGODB_URL,
            database_name=settings.MONGODB_DB
        )
        

    except Exception as e:
        raise RuntimeError(f"❌ Startup error: {str(e)}")

    # Yield control to run the app
    yield

    # ---- SHUTDOWN ----
    await mongo_connector.close()
    print("🧹 App shutdown: MongoDB connection closed")