#!/usr/bin/env python3

import requests
import json

# Test script for the Music Library API
BASE_URL = "http://localhost:5000/api"

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_add_song():
    """Test adding a new song"""
    print("Testing add song...")
    song_data = {
        "title": "Bohemian Rhapsody",
        "artist": "Queen",
        "album": "A Night at the Opera",
        "genre": "Rock",
        "year": "1975",
        "duration": "5:55"
    }
    
    response = requests.post(f"{BASE_URL}/songs", json=song_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {result}")
    return result.get('song', {}).get('id')

def test_get_songs():
    """Test getting all songs"""
    print("Testing get all songs...")
    response = requests.get(f"{BASE_URL}/songs")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Total songs: {len(result['songs'])}")
    for song in result['songs']:
        print(f"  - {song['title']} by {song['artist']}")
    print()

def test_search_songs():
    """Test searching songs"""
    print("Testing search songs...")
    response = requests.get(f"{BASE_URL}/songs/search?q=queen")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Search results: {len(result['songs'])}")
    for song in result['songs']:
        print(f"  - {song['title']} by {song['artist']}")
    print()

def test_stats():
    """Test getting library stats"""
    print("Testing library stats...")
    response = requests.get(f"{BASE_URL}/stats")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Stats: {result}")
    print()

if __name__ == "__main__":
    print("Music Library API Test Script")
    print("=" * 40)
    
    try:
        test_health()
        song_id = test_add_song()
        test_get_songs()
        test_search_songs()
        test_stats()
        print("All tests completed successfully!")
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to the API. Make sure the server is running on localhost:5000")
    except Exception as e:
        print(f"Error: {e}")