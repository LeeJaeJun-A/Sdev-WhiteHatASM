from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.database.database import SessionLocal
from backend.database.init_database import init_database
from backend.routes import authentication
from backend.routes import user
from backend.routes import crawl
from backend.routes import websocket
from backend.routes import test
from backend.routes import history
from backend.routes import report
from backend.routes import contact

app = FastAPI()

# Define CORS settings to allow requests from specified origins
origins = [
    "http://localhost:4173",
    "http://localhost:5173",
    "http://127.0.0.1:4173",
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from these origins
    allow_credentials=True,  # Allow credentials to be sent
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(authentication.router, tags=["login"])
app.include_router(user.router, tags=["user"])
app.include_router(crawl.router, tags=["crawler"])
app.include_router(websocket.router, tags=["websocket"])
app.include_router(test.router, tags=["test"])
app.include_router(history.router, tags=["history"])
app.include_router(report.router, tags=["report"])
app.include_router(contact.router, tags=["contact"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        init_database(db)
        yield
    finally:
        db.close()


app.router.lifespan_context = lifespan


@app.get("/")
def read_root():
    return {"message": "Hello World!"}
