from sqlalchemy import create_engine, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional
import os

from ..models.song import Song, SongCreate, SongUpdate

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SongService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_songs(self, skip: int = 0, limit: int = 100) -> List[Song]:
        """Get all songs with pagination"""
        return self.db.query(Song).offset(skip).limit(limit).all()
    
    def get_song(self, song_id: int) -> Optional[Song]:
        """Get a song by ID"""
        return self.db.query(Song).filter(Song.id == song_id).first()
    
    def create_song(self, song: SongCreate) -> Song:
        """Create a new song"""
        db_song = Song(**song.model_dump())
        self.db.add(db_song)
        self.db.commit()
        self.db.refresh(db_song)
        return db_song
    
    def update_song(self, song_id: int, song_update: SongUpdate) -> Optional[Song]:
        """Update an existing song"""
        db_song = self.get_song(song_id)
        if db_song:
            update_data = song_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_song, field, value)
            self.db.commit()
            self.db.refresh(db_song)
        return db_song
    
    def delete_song(self, song_id: int) -> bool:
        """Delete a song"""
        db_song = self.get_song(song_id)
        if db_song:
            self.db.delete(db_song)
            self.db.commit()
            return True
        return False
    
    def search_songs(self, query: str) -> List[Song]:
        """Search songs by title, artist, album, or genre"""
        return self.db.query(Song).filter(
            or_(
                Song.title.contains(query),
                Song.artist.contains(query),
                Song.album.contains(query),
                Song.genre.contains(query)
            )
        ).all()
    
    def get_songs_by_artist(self, artist: str) -> List[Song]:
        """Get all songs by a specific artist"""
        return self.db.query(Song).filter(Song.artist.ilike(f"%{artist}%")).all()
    
    def get_songs_by_genre(self, genre: str) -> List[Song]:
        """Get all songs by a specific genre"""
        return self.db.query(Song).filter(Song.genre.ilike(f"%{genre}%")).all()
