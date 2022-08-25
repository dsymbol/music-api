import uvicorn
from fastapi import FastAPI

import src.album as album
import src.artist as artist
import src.song as song

app = FastAPI(
    docs_url="/",
    redoc_url=None,
    title="music-api",
    contact={"name": "dsymbol", "url": "http://github.com/dsymbol/music-api"},
)

app.include_router(router=artist.router, tags=["Artist"], prefix="/api/artist")
app.include_router(router=album.router, tags=["Album"], prefix="/api/album")
app.include_router(router=song.router, tags=["Song"], prefix="/api/song")

if __name__ == "__main__":
    uvicorn.run(
        "server:app", host="127.0.0.1", port=5000, log_level="info", reload=True
    )
