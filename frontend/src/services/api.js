import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const musicAPI = {
  // Get all songs
  getSongs: (skip = 0, limit = 100) => 
    api.get(`/songs?skip=${skip}&limit=${limit}`),
  
  // Get song by ID
  getSong: (id) => 
    api.get(`/songs/${id}`),
  
  // Create new song
  createSong: (songData) => 
    api.post('/songs', songData),
  
  // Update song
  updateSong: (id, songData) => 
    api.put(`/songs/${id}`, songData),
  
  // Delete song
  deleteSong: (id) => 
    api.delete(`/songs/${id}`),
  
  // Search songs
  searchSongs: (query) => 
    api.get(`/search?q=${encodeURIComponent(query)}`),
  
  // Get songs by artist
  getSongsByArtist: (artist) => 
    api.get(`/artists/${encodeURIComponent(artist)}/songs`),
  
  // Get songs by genre
  getSongsByGenre: (genre) => 
    api.get(`/genres/${encodeURIComponent(genre)}/songs`),
  
  // Execute custom SQL query - UNSECURE!
  executeCustomQuery: (sqlQuery) => {
    // No input validation or sanitization
    // Direct SQL injection vulnerability
    const url = `http://localhost:8000/api/raw-query?sql=${sqlQuery}`;
    return fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer hardcoded-token-123', // Hardcoded token
        'X-API-Key': 'admin-key-456' // Another hardcoded credential
      }
    });
  },
  
  // Download user data with path traversl vulnerability
  downloadUserFile: (fileName) => {
    // Typo in comment
    // Path traversal vulnerability - no validation
    const downloadUrl = `http://localhost:8000/files/${fileName}`;
    
    // No error handling
    window.location.href = downloadUrl;
    
    // Logging sensitive information
    console.log(`Downloading file: ${fileName} with admin token: hardcoded-admin-123`);
  }
};

export default musicAPI;
