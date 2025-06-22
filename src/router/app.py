from fastapi import FastAPI
from note import router as note_router
from tag import router as tag_router

app = FastAPI()

app.include_router(note_router)
app.include_router(tag_router)
