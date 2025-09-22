"""
Script to add sample music data for testing the Music Library application
"""
import sys
import os

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.song import Song, Base

# Sample songs data
SAMPLE_SONGS = [
    {
        "title": "Bohemian Rhapsody",
        "artist": "Queen",
        "album": "A Night at the Opera",
        "genre": "Rock",
        "year": 1975,
        "duration": 355,
        "artwork_url": "https://example.com/queen-bohemian.jpg"
    },
    {
        "title": "Stairway to Heaven", 
        "artist": "Led Zeppelin",
        "album": "Led Zeppelin IV",
        "genre": "Rock",
        "year": 1971,
        "duration": 482
    },
    {
        "title": "Hotel California",
        "artist": "Eagles",
        "album": "Hotel California", 
        "genre": "Rock",
        "year": 1976,
        "duration": 391
    },
    {
        "title": "Imagine",
        "artist": "John Lennon",
        "album": "Imagine",
        "genre": "Pop",
        "year": 1971,
        "duration": 183
    },
    {
        "title": "Billie Jean",
        "artist": "Michael Jackson", 
        "album": "Thriller",
        "genre": "Pop",
        "year": 1983,
        "duration": 294
    },
    {
        "title": "Sweet Child O' Mine",
        "artist": "Guns N' Roses",
        "album": "Appetite for Destruction",
        "genre": "Hard Rock", 
        "year": 1987,
        "duration": 356
    },
    {
        "title": "Like a Rolling Stone",
        "artist": "Bob Dylan",
        "album": "Highway 61 Revisited", 
        "genre": "Folk Rock",
        "year": 1965,
        "duration": 369
    },
    {
        "title": "Smells Like Teen Spirit",
        "artist": "Nirvana",
        "album": "Nevermind",
        "genre": "Grunge",
        "year": 1991,
        "duration": 301
    }
]


def add_sample_data():
    """Add sample songs to the database"""
    # Database setup
    DATABASE_URL = "sqlite:///./database.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        # Check if data already exists
        existing_count = session.query(Song).count()
        if existing_count > 0:
            print(f"📀 Database already has {existing_count} songs. Skipping sample data insertion.")
            return
        
        # Add sample songs
        print("🎵 Adding sample music data...")
        
        for song_data in SAMPLE_SONGS:
            song = Song(**song_data)
            session.add(song)
            print(f"  ✅ Added: {song_data['title']} by {song_data['artist']}")
        
        session.commit()
        
        # Verify insertion
        total_songs = session.query(Song).count()
        print(f"🎉 Successfully added {len(SAMPLE_SONGS)} sample songs!")
        print(f"📊 Total songs in database: {total_songs}")
        
        # Show some stats
        genres = session.query(Song.genre).distinct().all()
        artists = session.query(Song.artist).distinct().all()
        print(f"🎨 Genres: {len([g[0] for g in genres if g[0]])}")
        print(f"🎤 Artists: {len([a[0] for a in artists if a[0]])}")
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    print("🎼 Music Library - Sample Data Generator")
    print("=" * 50)
    add_sample_data()
