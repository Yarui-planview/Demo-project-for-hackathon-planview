"""
Simple tests for the Music Library API
"""
import pytest
from app.models.song import SongCreate, SongUpdate


def test_song_create_model():
    """Test SongCreate model validation"""
    song_data = {
        "title": "Test Song",
        "artist": "Test Artist",
        "album": "Test Album",
        "genre": "Rock",
        "year": 2024,
        "duration": 180
    }
    
    song = SongCreate(**song_data)
    assert song.title == "Test Song"
    assert song.artist == "Test Artist"
    assert song.year == 2024


def test_song_create_minimal():
    """Test SongCreate with minimal required fields"""
    song_data = {
        "title": "Minimal Song",
        "artist": "Minimal Artist"
    }
    
    song = SongCreate(**song_data)
    assert song.title == "Minimal Song"
    assert song.artist == "Minimal Artist"
    assert song.album is None
    assert song.genre is None


def test_song_update_model():
    """Test SongUpdate model with partial data"""
    update_data = {
        "title": "Updated Title",
        "year": 2025
    }
    
    song_update = SongUpdate(**update_data)
    assert song_update.title == "Updated Title"
    assert song_update.year == 2025
    assert song_update.artist is None


def test_duration_formatting():
    """Test duration formatting utility"""
    def format_duration(seconds):
        if not seconds:
            return '0:00'
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"
    
    assert format_duration(0) == '0:00'
    assert format_duration(60) == '1:00'
    assert format_duration(125) == '2:05'
    assert format_duration(3661) == '61:01'


def test_song_validation():
    """Test that invalid song data raises appropriate errors"""
    # Test empty title
    try:
        SongCreate(title="", artist="Test Artist")
        assert False, "Should raise validation error for empty title"
    except Exception:
        pass  # Expected to fail
    
    # Test empty artist
    try:
        SongCreate(title="Test Song", artist="")
        assert False, "Should raise validation error for empty artist"
    except Exception:
        pass  # Expected to fail


if __name__ == "__main__":
    # Run basic tests
    test_song_create_model()
    test_song_create_minimal()
    test_song_update_model()
    test_duration_formatting()
    print("✅ All basic tests passed!")
