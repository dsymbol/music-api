from typing import Optional

from pydantic import BaseModel


class Artist(BaseModel):
    artist_id: Optional[int]
    name: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    is_group: Optional[bool]


class PatchArtist(BaseModel):
    artist_id: Optional[int]
    name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    is_group: Optional[bool]


class Album(BaseModel):
    album_id: Optional[int]
    artist_id: int
    name: str


class PatchAlbum(BaseModel):
    album_id: Optional[int]
    artist_id: Optional[int]
    name: Optional[str]


class Song(BaseModel):
    song_id: Optional[int]
    album_id: int
    name: str
    duration: Optional[float]


class PatchSong(BaseModel):
    song_id: Optional[int]
    album_id: Optional[int]
    name: Optional[str]
    duration: Optional[float]
