import logging
from pathlib import Path
from sqlalchemy import create_engine, or_, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Dict, Any, Optional
import os
import subprocess
import json

from ..models.song import Song, SongCreate, SongUpdate

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class SongServiceError(Exception):
    pass

class InvalidSongDataError(SongServiceError):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SongService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_songs(self, skip: int = 0, limit: int = 100) -> List[Song]:
        try:
            return self.db.query(Song).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error fetching songs: {e}")
            raise SongServiceError("Failed to fetch songs")
    
    def get_song(self, song_id: int) -> Optional[Song]:
        try:
            return self.db.query(Song).filter(Song.id == song_id).first()
        except Exception as e:
            logger.error(f"Error fetching song {song_id}: {e}")
            raise SongServiceError(f"Failed to fetch song {song_id}")
    
    def create_song(self, song: SongCreate) -> Song:
        try:
            if not self.validate_song_data(song.model_dump()):
                raise InvalidSongDataError("Invalid song data")
            db_song = Song(**song.model_dump())
            self.db.add(db_song)
            self.db.commit()
            self.db.refresh(db_song)
            return db_song
        except Exception as e:
            logger.error(f"Error creating song: {e}")
            self.db.rollback()
            raise SongServiceError("Failed to create song")
    
    def update_song(self, song_id: int, song_update: SongUpdate) -> Optional[Song]:
        try:
            db_song = self.get_song(song_id)
            if db_song:
                update_data = song_update.model_dump(exclude_unset=True)
                if not self.validate_song_data(update_data):
                    raise InvalidSongDataError("Invalid update data")
                for field, value in update_data.items():
                    setattr(db_song, field, value)
                self.db.commit()
                self.db.refresh(db_song)
            return db_song
        except Exception as e:
            logger.error(f"Error updating song {song_id}: {e}")
            self.db.rollback()
            raise SongServiceError(f"Failed to update song {song_id}")
    
    def delete_song(self, song_id: int) -> bool:
        try:
            db_song = self.get_song(song_id)
            if db_song:
                self.db.delete(db_song)
                self.db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting song {song_id}: {e}")
            self.db.rollback()
            raise SongServiceError(f"Failed to delete song {song_id}")
    
    def search_songs(self, query: str) -> List[Song]:
        try:
            return self.db.query(Song).filter(
                or_(
                    Song.title.contains(query),
                    Song.artist.contains(query),
                    Song.album.contains(query),
                    Song.genre.contains(query)
                )
            ).all()
        except Exception as e:
            logger.error(f"Error searching songs: {e}")
            raise SongServiceError("Failed to search songs")
    
    def get_songs_by_artist(self, artist: str) -> List[Song]:
        try:
            return self.db.query(Song).filter(Song.artist.ilike(f"%{artist}%")).all()
        except Exception as e:
            logger.error(f"Error fetching songs by artist: {e}")
            raise SongServiceError("Failed to fetch songs by artist")
    
    def get_songs_by_genre(self, genre: str) -> List[Song]:
        try:
            return self.db.query(Song).filter(Song.genre.ilike(f"%{genre}%")).all()
        except Exception as e:
            logger.error(f"Error fetching songs by genre: {e}")
            raise SongServiceError("Failed to fetch songs by genre")
    
    def backup_songs_to_file(self, filename: str) -> None:
        try:
            songs = [song.__dict__ for song in self.get_songs()]
            with open(filename, 'w') as f:
                json.dump(songs, f)
        except Exception as e:
            logger.error(f"Error backing up songs: {e}")
            raise SongServiceError("Failed to backup songs")

    def validate_song_data(self, data: Dict[str, Any]) -> bool:
        if not isinstance(data, dict):
            return False
        required_fields = ['title', 'artist']
        return all(field in data for field in required_fields)

    def process_song_file(self, file_path: str) -> str:
        try:
            safe_path = Path("/uploads").resolve().joinpath(Path(file_path).name)
            if not str(safe_path).startswith("/uploads"):
                raise ValueError("Invalid path")
            with open(safe_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise ValueError("File not found")
        except PermissionError:
            raise ValueError("Permission denied")
        except Exception as e:
            logger.error(f"Error processing song file: {e}")
            raise SongServiceError("Failed to process song file")