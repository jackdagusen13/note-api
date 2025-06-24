from fastapi import FastAPI
from src.router.note import router as note_router
from src.router.tag import router as tag_router

app = FastAPI()

app.include_router(note_router)
app.include_router(tag_router)



@app.get("/")
def health_check():
    return {"status": "ok", "message": "API is running"}
