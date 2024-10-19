from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from . database import engine
from . routers import post, user, auth, votes
from . config import Settings

# This line is responsible in creating all our ORM models automatically if they do not exists
# If they exists it will not. But for automatic database manage for changes we used alembic
'''
models.Base.metadata.create_all(bind=engine)
'''

# This is the FastAPI app
app = FastAPI()

# CORS SETUP
# YOU SPECIFY THE DOMAIN LIST THAT YOU WANT TO ALLOW

# SPECIFIC DOMAIN
'''
origins = [
    ".....",
    ".....",
    ".....",
    ".....",
    ".....",
]
'''
# EVERY SINGLE DOMAIN - PUBLIC API
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # METHODS: GET, POST, PUT, DELETE etc. (*) FOR ALL
    allow_headers=["*"],  # SPECIFY HEADERS TO ALLOW
)


# Calling the routers created in routers folder in the main
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(votes.router)
app.include_router(user.router)


@app.get("/", tags=['Welcome'])
def root():
    return {"message": "WELCOME TO MY API PROJECT UPDATED"}
