from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import thumbnail, images

app = FastAPI()
app.include_router(thumbnail.router)
app.include_router(images.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/")
def home():
    return "Hi this is file service"


