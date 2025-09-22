#!/usr/bin/env python3
"""
Sample data seeder for Music Library
Adds some test songs to demonstrate the application features
"""

import requests
import json
from typing import List, Dict

# Sample songs data
SAMPLE_SONGS = [
    {
        "title": "Bohemian Rhapsody",
        "artist": "Queen", 
        "album": "A Night at the Opera",
        "genre": "Rock",
        "year": 1975,
        "duration": 355,
        "artwork_url": "https://upload.wikimedia.org/wikipedia/en/4/4d/Queen_A_Night_at_the_Opera.png"
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
        "title": "Smells Like Teen Spirit",
        "artist": "Nirvana",
        "album": "Nevermind",
        "genre": "Grunge",
        "year": 1991,
        "duration": 301
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
        "title": "Wonderwall",
        "artist": "Oasis",
        "album": "(What's the Story) Morning Glory?",
        "genre": "Britpop",
        "year": 1995,
        "duration": 258
    }
]

def add_sample_data(base_url: str = "http://localhost:8000") -> None:
    """Add sample songs to the music library"""
    print("🎵 Adding sample songs to Music Library...")
    
    added_count = 0
    failed_count = 0
    
    for song_data in SAMPLE_SONGS:
        try:
            response = requests.post(
                f"{base_url}/api/songs",
                json=song_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                print(f"✅ Added: {song_data['title']} by {song_data['artist']}")
                added_count += 1
            else:
                print(f"❌ Failed to add {song_data['title']}: {response.status_code}")
                failed_count += 1
                
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to the backend server.")
            print("   Make sure the backend is running on http://localhost:8000")
            return
        except Exception as e:
            print(f"❌ Error adding {song_data['title']}: {str(e)}")
            failed_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Successfully added: {added_count} songs")
    print(f"   ❌ Failed to add: {failed_count} songs")
    print(f"   🎵 Total sample songs: {len(SAMPLE_SONGS)}")

def check_server_status(base_url: str = "http://localhost:8000") -> bool:
    """Check if the backend server is running"""
    try:
        response = requests.get(f"{base_url}/health")
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    print("🎶 Music Library Sample Data Seeder")
    print("=" * 40)
    
    # Check if server is running
    if not check_server_status():
        print("❌ Backend server is not running!")
        print("   Please start the backend server first:")
        print("   cd backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000")
        exit(1)
    
    print("✅ Backend server is running")
    add_sample_data()
    print("\n🎉 Sample data seeding complete!")
    print("   Visit http://localhost:5173 to see your music library!")
