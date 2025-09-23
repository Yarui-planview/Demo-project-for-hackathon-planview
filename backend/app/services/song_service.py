Here's the fixed code for the identified issues in the changed lines, specifically addressing the path traversal vulnerability and redundant path resolution:

```python
def process_song_file(self, file_path: str) -> str:
    try:
        base_path = os.path.abspath('/uploads')
        safe_path = os.path.abspath(os.path.join(base_path, os.path.basename(file_path)))
        
        # Ensure the resolved path is within the uploads directory
        if not safe_path.startswith(base_path):
            raise ValueError("Invalid path - attempted directory traversal")
            
        # Validate file extension
        allowed_extensions = {'.mp3', '.wav', '.flac'}
        if not os.path.splitext(safe_path)[1].lower() in allowed_extensions:
            raise ValueError("Invalid file type")
            
        if not os.path.exists(safe_path):
            raise FileNotFoundError("File not found")
            
        with open(safe_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        raise ValueError("File not found")
    except PermissionError:
        raise ValueError("Permission denied")
    except Exception as e:
        logger.error(f"Error processing song file: {e}")
        raise SongServiceError("Failed to process song file")

```diff
-    def validate_song_data(self, data: Dict[str, Any]) -> bool:
+    def validate_song_data(self, data: Dict[str, Any]) -> bool:
         if not isinstance(data, dict):
             return False
         required_fields = ['title', 'artist']
-        return all(field in data for field in required_fields)
+        return all(field in data and isinstance(data[field], str) for field in required_fields)

     def process_song_file(self, file_path: str) -> str:
         try:
-            safe_path = Path("/uploads").resolve().joinpath(Path(file_path).name)
+            base_path = Path("/uploads").resolve()
+            safe_path = os.path.realpath(os.path.join(base_path, os.path.basename(file_path)))
             if not str(safe_path).startswith("/uploads"):
                 raise ValueError("Invalid path")
+            if not os.path.exists(safe_path):
+                raise FileNotFoundError("File not found")
             with open(safe_path, 'r') as f:
                 return f.read()
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