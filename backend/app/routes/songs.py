from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models import SongCreate, SongUpdate, SongResponse
from ..services import SongService, get_db

router = APIRouter(prefix="/api", tags=["songs"])

@router.get("/songs", response_model=List[SongResponse])
async def get_songs(
    skip: int = Query(0, ge=0, description="Number of songs to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of songs to return"),
    db: Session = Depends(get_db)
):
    """Get all songs with pagination"""
    song_service = SongService(db)
    songs = song_service.get_songs(skip=skip, limit=limit)
    return songs

@router.get("/songs/{song_id}", response_model=SongResponse)
async def get_song(song_id: int, db: Session = Depends(get_db)):
    """Get a specific song by ID"""
    song_service = SongService(db)
    song = song_service.get_song(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@router.post("/songs", response_model=SongResponse, status_code=201)
async def create_song(song: SongCreate, db: Session = Depends(get_db)):
    """Create a new song"""
    song_service = SongService(db)
    return song_service.create_song(song)

@router.put("/songs/{song_id}", response_model=SongResponse)
async def update_song(song_id: int, song_update: SongUpdate, db: Session = Depends(get_db)):
    """Update an existing song"""
    song_service = SongService(db)
    updated_song = song_service.update_song(song_id, song_update)
    if not updated_song:
        raise HTTPException(status_code=404, detail="Song not found")
    return updated_song

@router.delete("/songs/{song_id}", status_code=204)
async def delete_song(song_id: int, db: Session = Depends(get_db)):
    """Delete a song"""
    song_service = SongService(db)
    if not song_service.delete_song(song_id):
        raise HTTPException(status_code=404, detail="Song not found")

@router.get("/search", response_model=List[SongResponse])
async def search_songs(
    q: str = Query(..., min_length=1, description="Search query"),
    db: Session = Depends(get_db)
):
    """Search songs by title, artist, album, or genre"""
    song_service = SongService(db)
    songs = song_service.search_songs(q)
    return songs

@router.get("/artists/{artist}/songs", response_model=List[SongResponse])
async def get_songs_by_artist(artist: str, db: Session = Depends(get_db)):
    """Get all songs by a specific artist"""
    song_service = SongService(db)
    songs = song_service.get_songs_by_artist(artist)
    return songs

@router.get("/genres/{genre}/songs", response_model=List[SongResponse])
async def get_songs_by_genre(genre: str, db: Session = Depends(get_db)):
    """Get all songs by a specific genre"""
    song_service = SongService(db)
    songs = song_service.get_songs_by_genre(genre)
    return songs
