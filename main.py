import uvicorn
import logging
from fastapi import FastAPI
from startup import lifespan
from api import all_routers
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Calculator Database Service",
    description="EC2 service for handling database operations with singleton MongoDB connection",
    version="1.0.0"
    , lifespan=lifespan)

origins = ["http://localhost:5173", "http://0.0.0.0:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


for r in all_routers:
    app.include_router(r, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080)
