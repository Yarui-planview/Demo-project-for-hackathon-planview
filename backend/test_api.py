"""
Unit tests for the Music Library API endpoints
Simple test file to demonstrate testing capabilities for the review bot
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models.song import Base
from app.services.song_service import get_db

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestMusicLibraryAPI:
    """Test class for Music Library API endpoints"""
    
    def test_root_endpoint(self):
        """Test the root endpoint returns correct response"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Welcome to Music Library API" in data["message"]
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_get_empty_songs(self):
        """Test getting songs from empty database"""
        response = client.get("/api/songs")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_song(self):
        """Test creating a new song"""
        song_data = {
            "title": "Test Song",
            "artist": "Test Artist",
            "album": "Test Album",
            "genre": "Test Genre",
            "year": 2024,
            "duration": 180
        }
        
        response = client.post("/api/songs", json=song_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == song_data["title"]
        assert data["artist"] == song_data["artist"]
        assert data["album"] == song_data["album"]
        assert "id" in data
        
        return data["id"]  # Return ID for use in other tests
    
    def test_get_song_by_id(self):
        """Test retrieving a song by ID"""
        # First create a song
        song_id = self.test_create_song()
        
        # Then retrieve it
        response = client.get(f"/api/songs/{song_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == song_id
        assert data["title"] == "Test Song"
    
    def test_get_nonexistent_song(self):
        """Test retrieving a non-existent song returns 404"""
        response = client.get("/api/songs/99999")
        assert response.status_code == 404
        
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_search_songs(self):
        """Test searching songs"""
        # Create a song first
        self.test_create_song()
        
        # Search for it
        response = client.get("/api/search?q=Test")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        # Should find our test song
        if len(data) > 0:
            assert "Test" in data[0]["title"] or "Test" in data[0]["artist"]
    
    def test_library_stats(self):
        """Test getting library statistics"""
        response = client.get("/api/stats")
        assert response.status_code == 200
        
        data = response.json()
        required_fields = [
            "total_songs", "total_artists", "total_albums", 
            "total_genres", "total_duration", "average_song_duration"
        ]
        
        for field in required_fields:
            assert field in data
            assert isinstance(data[field], (int, type(None)))
    
    def test_create_song_validation(self):
        """Test song creation with invalid data"""
        # Test missing required fields
        incomplete_song = {
            "title": "Test Song"
            # Missing required 'artist' field
        }
        
        response = client.post("/api/songs", json=incomplete_song)
        assert response.status_code == 422  # Validation error
    
    def test_update_song(self):
        """Test updating a song"""
        # Create a song first
        song_id = self.test_create_song()
        
        # Update it
        update_data = {
            "title": "Updated Test Song",
            "genre": "Updated Genre"
        }
        
        response = client.put(f"/api/songs/{song_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == "Updated Test Song"
        assert data["genre"] == "Updated Genre"
        assert data["artist"] == "Test Artist"  # Should remain unchanged
    
    def test_delete_song(self):
        """Test deleting a song"""
        # Create a song first
        song_id = self.test_create_song()
        
        # Delete it
        response = client.delete(f"/api/songs/{song_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        response = client.get(f"/api/songs/{song_id}")
        assert response.status_code == 404

# Integration test
def test_full_crud_workflow():
    """Test complete Create-Read-Update-Delete workflow"""
    song_data = {
        "title": "Workflow Test Song",
        "artist": "Workflow Artist",
        "album": "Workflow Album",
        "genre": "Test",
        "year": 2024,
        "duration": 200
    }
    
    # Create
    response = client.post("/api/songs", json=song_data)
    assert response.status_code == 201
    song_id = response.json()["id"]
    
    # Read
    response = client.get(f"/api/songs/{song_id}")
    assert response.status_code == 200
    assert response.json()["title"] == song_data["title"]
    
    # Update
    update_data = {"title": "Updated Workflow Song"}
    response = client.put(f"/api/songs/{song_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Workflow Song"
    
    # Delete
    response = client.delete(f"/api/songs/{song_id}")
    assert response.status_code == 204
    
    # Verify deletion
    response = client.get(f"/api/songs/{song_id}")
    assert response.status_code == 404

if __name__ == "__main__":
    # Simple test runner
    print("🧪 Running Music Library API Tests...")
    print("=" * 50)
    
    test_instance = TestMusicLibraryAPI()
    
    # Run basic tests
    tests = [
        ("Root Endpoint", test_instance.test_root_endpoint),
        ("Health Check", test_instance.test_health_endpoint), 
        ("Get Empty Songs", test_instance.test_get_empty_songs),
        ("Library Stats", test_instance.test_library_stats),
        ("Full CRUD Workflow", test_full_crud_workflow)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            print(f"✅ {test_name}")
            passed += 1
        except Exception as e:
            print(f"❌ {test_name}: {str(e)}")
            failed += 1
    
    print("=" * 50)
    print(f"🧪 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above.")
