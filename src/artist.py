from typing import List

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.interact import query
from src.models import Artist, PatchArtist

router = APIRouter()


@router.get("", response_model=List[Artist])
def read_all(
        id: int = None,
        name: str = None,
        first_name: str = None,
        last_name: str = None,
        group: bool = None,
):
    parts, params = [], []
    if id:
        parts.append("artist_id = ?")
        params.append(id)
    if name:
        parts.append("LOWER(name) = ?")
        params.append(name.lower())
    if first_name:
        parts.append("LOWER(first_name) = ?")
        params.append(first_name.lower())
    if last_name:
        parts.append("LOWER(last_name) = ?")
        params.append(last_name.lower())
    if group or group == False:
        parts.append("is_group = ?")
        params.append(group)
    if parts and params:
        where_str = " AND ".join(parts)
        statement = f"SELECT * FROM artist WHERE {where_str}"
        result = query(statement, *params)
    else:
        result = query("SELECT * FROM artist")
    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=format_data(result))


@router.get("/{id}", response_model=List[Artist])
def read(id: int):
    result = _read_id(id)
    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.get("/{id}/albums")
def read_albums(id: int):
    result = query(
        """
    SELECT artist.name, album.album_id, album.name
    FROM artist JOIN album WHERE artist.artist_id = ? 
    AND artist.artist_id = album.artist_id;
    """,
        id,
    )
    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )
    formatted = [{"album_id": i[1], "name": i[2]} for i in result]
    return JSONResponse(status_code=status.HTTP_200_OK, content=formatted)


@router.get("/{id}/songs")
def read_songs(id: int, album_id: int = None):
    params = [id]
    q = """
    SELECT artist.name, song.song_id, 
    song.name, album.name
    FROM artist JOIN album JOIN song
    WHERE artist.artist_id = ? 
    AND artist.artist_id = album.artist_id 
    AND album.album_id = song.album_id
    """
    if album_id:
        q += "AND album.album_id = ?"
        params.append(album_id)
    result = query(q, *params)
    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )
    formatted = [{"song_id": i[1], "album": i[3], "name": i[2]} for i in result]
    return JSONResponse(status_code=status.HTTP_200_OK, content=formatted)


@router.post("", response_model=List[Artist])
def create(payload: Artist):
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
            _read_id(payload.artist_id)
            if payload.artist_id
            else _read_id(
                query(
                    """SELECT artist_id FROM artist ORDER BY artist_id DESC LIMIT 1"""
                )[0][0]
            )
        )
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )


@router.delete("/{id}")
def delete(id: int):
    result = query("""DELETE FROM artist WHERE artist_id = ?""", id)
    if result > 0:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Artist deleted"}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )


@router.put("/{id}", response_model=List[Artist])
def update(id, payload: Artist):
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
        content = _read_id(payload.artist_id) if payload.artist_id else _read_id(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )


@router.patch("/{id}", response_model=List[Artist])
def partial_update(id, payload: PatchArtist):
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
        content = _read_id(payload.artist_id) if payload.artist_id else _read_id(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"}
        )


def payload_to_query(payload, id: int = None):
    parts, params = [], []
    if payload.artist_id:
        parts.append("artist_id")
        params.append(payload.artist_id)
    if payload.name:
        parts.append("name")
        params.append(payload.name)
    if payload.first_name:
        parts.append("first_name")
        params.append(payload.first_name)
    if payload.last_name:
        parts.append("last_name")
        params.append(payload.last_name)
    if payload.phone:
        parts.append("phone")
        params.append(payload.phone)
    if payload.website:
        parts.append("website")
        params.append(payload.website)
    if payload.is_group or payload.is_group == False:
        parts.append("is_group")
        params.append(payload.is_group)
    if parts and params:
        if id:
            parts = " = ?, ".join(parts)
            parts += " = ?"
            params.append(id)
            statement = f"""UPDATE artist SET {parts} WHERE artist_id = ?"""
        else:
            statement = f"""
                INSERT INTO artist ({", ".join(parts)})
                VALUES ({", ".join(["?" for _ in range(len(params))])})
                """
        return statement, params


def _read_id(id):
    result = query("SELECT * FROM artist WHERE artist_id = ?", id)
    return format_data(result)


def format_data(data: List[tuple]):
    """
    Returns formatted data in easily accessible dictionary format
    """
    l = []
    for i in data:
        artist_id, name, first_name, last_name, phone, website, is_group = i
        l.append(
            {
                "artist_id": artist_id,
                "name": name,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "website": website,
                "is_group": True if is_group == 1 else False,
            }
        )
    return l
