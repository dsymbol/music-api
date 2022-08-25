from typing import List

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.interact import query
from src.models import Album, PatchAlbum

router = APIRouter()


@router.get("", response_model=List[Album])
def read_all(id: int = None, artist_id: int = None, name: str = None):
    parts, params = [], []
    if id:
        parts.append("album_id = ?")
        params.append(id)
    if artist_id:
        parts.append("artist_id = ?")
        params.append(artist_id)
    if name:
        parts.append("lower(name) = ?")
        params.append(name.lower())
    if parts and params:
        where_str = " AND ".join(parts)
        statement = f"SELECT * FROM album WHERE {where_str}"
        result = query(statement, *params)
    else:
        result = query("SELECT * FROM album")
    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=format_data(result))


@router.get("/{id}", response_model=List[Album])
def read(id: int):
    result = _read_id(id)
    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.get("/{id}/songs")
def read_songs(id: int):
    result = query(
        """
    SELECT album.name, song.song_id, song.name
    FROM album JOIN song
    WHERE album.album_id = ?
    AND album.album_id = song.album_id
    """,
        id,
    )
    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )
    formatted = [{"song_id": i[1], "album": i[0], "name": i[2]} for i in result]
    return JSONResponse(status_code=status.HTTP_200_OK, content=formatted)


@router.post("", response_model=List[Album])
def create(payload: Album):
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
            _read_id(payload.album_id)
            if payload.album_id
            else _read_id(
                query("""SELECT album_id FROM album ORDER BY album_id DESC LIMIT 1""")[
                    0
                ][0]
            )
        )
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )


@router.delete("/{id}")
def delete(id: int):
    result = query("""DELETE FROM album WHERE album_id = ?""", id)
    if result > 0:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Album deleted"}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )


@router.put("/{id}", response_model=List[Album])
def update(id, payload: Album):
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
        content = _read_id(payload.album_id) if payload.album_id else _read_id(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )


@router.patch("/{id}", response_model=List[Album])
def partial_update(id, payload: PatchAlbum):
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
        content = _read_id(payload.album_id) if payload.album_id else _read_id(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )


def payload_to_query(payload, id: int = None):
    parts, params = [], []
    if payload.album_id:
        parts.append("album_id")
        params.append(payload.album_id)
    if payload.artist_id:
        parts.append("artist_id")
        params.append(payload.artist_id)
    if payload.name:
        parts.append("name")
        params.append(payload.name)
    if parts and params:
        if id:
            parts = " = ?, ".join(parts)
            parts += " = ?"
            params.append(id)
            statement = f"""UPDATE album SET {parts} WHERE album_id = ?"""
        else:
            statement = f"""
                INSERT INTO album ({", ".join(parts)})
                VALUES ({", ".join(["?" for _ in range(len(params))])})
                """
        return statement, params


def _read_id(id):
    result = query("SELECT * FROM album WHERE album_id = ?", id)
    return format_data(result)


def format_data(data: List[tuple]):
    """
    Returns formatted data in easily accessible dictionary format
    """
    l = []
    for i in data:
        album_id, artist_id, name = i
        l.append({"album_id": album_id, "artist_id": artist_id, "name": name})
    return l
