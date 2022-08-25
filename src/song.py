from typing import List

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.interact import query
from src.models import Song, PatchSong

router = APIRouter()


@router.get("", response_model=List[Song])
def read_all(id: int = None, album_id: int = None, name: str = None):
    parts, params = [], []
    if id:
        parts.append("song_id = ?")
        params.append(id)
    if album_id:
        parts.append("album_id = ?")
        params.append(album_id)
    if name:
        parts.append("lower(name) = ?")
        params.append(name.lower())
    if parts and params:
        where_str = " AND ".join(parts)
        statement = f"SELECT * FROM song WHERE {where_str}"
        result = query(statement, *params)
    else:
        result = query("SELECT * FROM song")
    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=format_data(result))


@router.get("/{id}", response_model=List[Song])
def read(id: int):
    result = _read_id(id)
    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.post("", response_model=List[Song])
def create(payload: Song):
    statement, params = payload_to_query(payload)
    try:
        result = query(statement, *params)
    except Exception as e:
        print(str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "message": "conflict with the current state of the target resource."
            },
        )
    if result > 0:
        content = (
            _read_id(payload.song_id)
            if payload.song_id
            else _read_id(
                query("""SELECT song_id FROM song ORDER BY song_id DESC LIMIT 1""")[0][
                    0
                ]
            )
        )
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )


@router.delete("/{id}")
def delete(id: int):
    result = query("""DELETE FROM song WHERE song_id = ?""", id)
    if result > 0:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Song deleted"}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )


@router.put("/{id}", response_model=List[Song])
def update(id, payload: Song):
    statement, params = payload_to_query(payload, id)
    try:
        result = query(statement, *params)
    except Exception as e:
        print(str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "message": "conflict with the current state of the target resource."
            },
        )
    if result > 0:
        content = _read_id(payload.song_id) if payload.song_id else _read_id(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )


@router.patch("/{id}", response_model=List[Song])
def partial_update(id, payload: PatchSong):
    statement, params = payload_to_query(payload, id)
    try:
        result = query(statement, *params)
    except Exception as e:
        print(str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "message": "conflict with the current state of the target resource."
            },
        )
    if result > 0:
        content = _read_id(payload.song_id) if payload.song_id else _read_id(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )


def payload_to_query(payload, id: int = None):
    parts, params = [], []
    if payload.song_id:
        parts.append("song_id")
        params.append(payload.song_id)
    if payload.album_id:
        parts.append("album_id")
        params.append(payload.album_id)
    if payload.name:
        parts.append("name")
        params.append(payload.name)
    if payload.duration:
        parts.append("duration")
        params.append(payload.duration)
    if parts and params:
        if id:
            parts = " = ?, ".join(parts)
            parts += " = ?"
            params.append(id)
            statement = f"""UPDATE song SET {parts} WHERE song_id = ?"""
        else:
            statement = f"""
                INSERT INTO song ({", ".join(parts)})
                VALUES ({", ".join(["?" for _ in range(len(params))])})
                """
        return statement, params


def _read_id(id):
    result = query("SELECT * FROM song WHERE song_id = ?", id)
    return format_data(result)


def format_data(data: List[tuple]):
    """
    Returns formatted data in easily accessible dictionary format
    """
    l = []
    for i in data:
        song_id, album_id, name, duration = i
        l.append(
            {
                "song_id": song_id,
                "album_id": album_id,
                "name": name,
                "duration": duration,
            }
        )
    return l
