import React, { useState, useEffect } from 'react';
import './App.css';
import MusicLibrary from './components/MusicLibrary';
import AddSong from './components/AddSong';
import SearchBar from './components/SearchBar';
import Stats from './components/Stats';
import { Song, LibraryStats } from './types';
import { musicAPI } from './services/api';

function App() {
  const [songs, setSongs] = useState<Song[]>([]);
  const [filteredSongs, setFilteredSongs] = useState<Song[]>([]);
  const [stats, setStats] = useState<LibraryStats | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadSongs = async () => {
    try {
      setLoading(true);
      const songsData = await musicAPI.getSongs();
      setSongs(songsData);
      setFilteredSongs(songsData);
    } catch (err) {
      setError('Failed to load songs');
      console.error('Error loading songs:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const statsData = await musicAPI.getStats();
      setStats(statsData);
    } catch (err) {
      console.error('Error loading stats:', err);
    }
  };

  useEffect(() => {
    loadSongs();
    loadStats();
  }, []);

  const handleAddSong = async (songData: Omit<Song, 'id' | 'date_added'>) => {
    try {
      await musicAPI.addSong(songData);
      await loadSongs();
      await loadStats();
      setShowAddForm(false);
    } catch (err) {
      setError('Failed to add song');
      console.error('Error adding song:', err);
    }
  };

  const handleDeleteSong = async (id: string) => {
    try {
      await musicAPI.deleteSong(id);
      await loadSongs();
      await loadStats();
    } catch (err) {
      setError('Failed to delete song');
      console.error('Error deleting song:', err);
    }
  };

  const handleSearch = async (query: string) => {
    if (!query.trim()) {
      setFilteredSongs(songs);
      return;
    }

    try {
      const results = await musicAPI.searchSongs(query);
      setFilteredSongs(results);
    } catch (err) {
      console.error('Error searching songs:', err);
      setFilteredSongs([]);
    }
  };

  if (loading) {
    return (
      <div className="App">
        <div className="loading">Loading music library...</div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎵 Music Library</h1>
        <p>Manage your personal music collection</p>
      </header>

      {error && (
        <div className="error-message">
          {error}
          <button onClick={() => setError(null)}>✖</button>
        </div>
      )}

      <main className="App-main">
        <div className="controls">
          <SearchBar onSearch={handleSearch} />
          <button 
            className="add-song-btn"
            onClick={() => setShowAddForm(!showAddForm)}
          >
            {showAddForm ? '← Back to Library' : '+ Add New Song'}
          </button>
        </div>

        {stats && <Stats stats={stats} />}

        {showAddForm ? (
          <AddSong 
            onAdd={handleAddSong} 
            onCancel={() => setShowAddForm(false)} 
          />
        ) : (
          <MusicLibrary 
            songs={filteredSongs} 
            onDelete={handleDeleteSong}
          />
        )}
      </main>
    </div>
  );
}

export default App;
