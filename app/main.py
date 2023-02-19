from fastapi import FastAPI
from . import  models
from .database import engine
from .routers import user_controller,word_controller, auth, vote_controller
from .confige import settings
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine) // it's job has been doing by alembic



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_controller.router)
app.include_router(word_controller.router)
app.include_router(auth.router)
app.include_router(vote_controller.router)

@app.get("/")
def root():
    return {"message":"Hello World"}






