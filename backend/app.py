from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

# In-memory storage for demonstration (in production, use a proper database)
music_library = []

# Data file for persistence
DATA_FILE = 'music_data.json'

def load_data():
    """Load music data from file"""
    global music_library
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                music_library = json.load(f)
        except:
            music_library = []

def save_data():
    """Save music data to file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(music_library, f, indent=2)

# Load existing data on startup
load_data()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Music Library API is running"})

@app.route('/api/songs', methods=['GET'])
def get_songs():
    """Get all songs in the library"""
    return jsonify({"songs": music_library})

@app.route('/api/songs', methods=['POST'])
def add_song():
    """Add a new song to the library"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'artist', 'album']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create new song entry
        song = {
            "id": str(uuid.uuid4()),
            "title": data['title'],
            "artist": data['artist'],
            "album": data['album'],
            "genre": data.get('genre', ''),
            "year": data.get('year', ''),
            "duration": data.get('duration', ''),
            "date_added": datetime.now().isoformat()
        }
        
        music_library.append(song)
        save_data()
        
        return jsonify({"message": "Song added successfully", "song": song}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/songs/<song_id>', methods=['GET'])
def get_song(song_id):
    """Get a specific song by ID"""
    song = next((s for s in music_library if s['id'] == song_id), None)
    if song:
        return jsonify({"song": song})
    return jsonify({"error": "Song not found"}), 404

@app.route('/api/songs/<song_id>', methods=['PUT'])
def update_song(song_id):
    """Update a song"""
    try:
        data = request.get_json()
        song = next((s for s in music_library if s['id'] == song_id), None)
        
        if not song:
            return jsonify({"error": "Song not found"}), 404
        
        # Update song fields
        song['title'] = data.get('title', song['title'])
        song['artist'] = data.get('artist', song['artist'])
        song['album'] = data.get('album', song['album'])
        song['genre'] = data.get('genre', song['genre'])
        song['year'] = data.get('year', song['year'])
        song['duration'] = data.get('duration', song['duration'])
        
        save_data()
        
        return jsonify({"message": "Song updated successfully", "song": song})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/songs/<song_id>', methods=['DELETE'])
def delete_song(song_id):
    """Delete a song"""
    global music_library
    song = next((s for s in music_library if s['id'] == song_id), None)
    
    if not song:
        return jsonify({"error": "Song not found"}), 404
    
    music_library = [s for s in music_library if s['id'] != song_id]
    save_data()
    
    return jsonify({"message": "Song deleted successfully"})

@app.route('/api/songs/search', methods=['GET'])
def search_songs():
    """Search songs by title, artist, album, or genre"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({"songs": music_library})
    
    filtered_songs = []
    for song in music_library:
        if (query in song['title'].lower() or 
            query in song['artist'].lower() or 
            query in song['album'].lower() or 
            query in song.get('genre', '').lower()):
            filtered_songs.append(song)
    
    return jsonify({"songs": filtered_songs})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get library statistics"""
    total_songs = len(music_library)
    artists = set(song['artist'] for song in music_library)
    albums = set(song['album'] for song in music_library)
    genres = set(song.get('genre', '') for song in music_library if song.get('genre'))
    
    return jsonify({
        "total_songs": total_songs,
        "total_artists": len(artists),
        "total_albums": len(albums),
        "total_genres": len(genres),
        "artists": list(artists),
        "genres": list(genres)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)