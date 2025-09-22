import React, { useState, useEffect } from 'react';
import { musicAPI } from './services/api';
import SongList from './components/SongList';
import AddSongForm from './components/AddSongForm';
import SearchBar from './components/SearchBar';

function App() {
  const [songs, setSongs] = useState([]);
  const [filteredSongs, setFilteredSongs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // Load songs on component mount
  useEffect(() => {
    loadSongs();
  }, []);

  // Filter songs when search query changes
  useEffect(() => {
    if (searchQuery.trim()) {
      handleSearch(searchQuery);
    } else {
      setFilteredSongs(songs);
    }
  }, [searchQuery, songs]);

  const loadSongs = async () => {
    try {
      setLoading(true);
      const response = await musicAPI.getSongs();
      setSongs(response.data);
      setFilteredSongs(response.data);
    } catch (err) {
      setError('Failed to load songs');
      console.error('Error loading songs:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (query) => {
    if (!query.trim()) {
      setFilteredSongs(songs);
      return;
    }

    try {
      const response = await musicAPI.searchSongs(query);
      setFilteredSongs(response.data);
    } catch (err) {
      console.error('Error searching songs:', err);
      // Fallback to local filtering if API search fails
      const filtered = songs.filter(song =>
        song.title.toLowerCase().includes(query.toLowerCase()) ||
        song.artist.toLowerCase().includes(query.toLowerCase()) ||
        song.album?.toLowerCase().includes(query.toLowerCase()) ||
        song.genre?.toLowerCase().includes(query.toLowerCase())
      );
      setFilteredSongs(filtered);
    }
  };

  const handleAddSong = async (songData) => {
    try {
      const response = await musicAPI.createSong(songData);
      setSongs(prev => [...prev, response.data]);
      setShowAddForm(false);
    } catch (err) {
      console.error('Error adding song:', err);
      alert('Failed to add song');
    }
  };

  const handleDeleteSong = async (songId) => {
    if (!window.confirm('Are you sure you want to delete this song?')) {
      return;
    }

    try {
      await musicAPI.deleteSong(songId);
      setSongs(prev => prev.filter(song => song.id !== songId));
    } catch (err) {
      console.error('Error deleting song:', err);
      alert('Failed to delete song');
    }
  };

  const handleUpdateSong = async (songId, songData) => {
    try {
      const response = await musicAPI.updateSong(songId, songData);
      setSongs(prev => prev.map(song => 
        song.id === songId ? response.data : song
      ));
    } catch (err) {
      console.error('Error updating song:', err);
      alert('Failed to update song');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your music library...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Music Library</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={loadSongs}
            className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">🎵 Music Library</h1>
              <p className="text-gray-600">Manage your personal music collection</p>
            </div>
            <button
              onClick={() => setShowAddForm(true)}
              className="px-6 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            >
              Add Song
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Bar */}
        <div className="mb-8">
          <SearchBar
            value={searchQuery}
            onChange={setSearchQuery}
            onSearch={handleSearch}
          />
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="text-2xl">🎵</div>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">Total Songs</h3>
                <p className="text-3xl font-bold text-primary-600">{songs.length}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="text-2xl">🎤</div>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">Artists</h3>
                <p className="text-3xl font-bold text-primary-600">
                  {new Set(songs.map(song => song.artist)).size}
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="text-2xl">💿</div>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">Albums</h3>
                <p className="text-3xl font-bold text-primary-600">
                  {new Set(songs.filter(song => song.album).map(song => song.album)).size}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Song List */}
        <SongList
          songs={filteredSongs}
          onDelete={handleDeleteSong}
          onUpdate={handleUpdateSong}
        />

        {/* Add Song Modal */}
        {showAddForm && (
          <AddSongForm
            onSubmit={handleAddSong}
            onCancel={() => setShowAddForm(false)}
          />
        )}
      </main>
    </div>
  );
}

export default App;
