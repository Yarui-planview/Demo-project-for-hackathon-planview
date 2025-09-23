import React, { useState } from 'react';

const SongList = ({ songs, onDelete, onUpdate }) => {
  const [editingSong, setEditingSong] = useState(null);
  const [editForm, setEditForm] = useState({});

  const formatDuration = (seconds) => {
    if (!seconds) return 'Unknown';
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleEdit = (song) => {
    setEditingSong(song.id);
    setEditForm(song);
  };

  const handleSaveEdit = () => {
    onUpdate(editingSong, editForm);
    setEditingSong(null);
    setEditForm({});
  };

  const handleCancelEdit = () => {
    setEditingSong(null);
    setEditForm({});
  };

  const handleEditChange = (field, value) => {
    setEditForm(prev => ({
      ...prev,
      [field]: value
    }));
  };

  if (songs.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-4xl mb-4">🎵</div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">No songs found</h3>
        <p className="text-gray-600">Your music library is empty - add some songs to get started!</p>
      </div>
    );
  }

  return (
    <div className="bg-white shadow rounded-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-lg font-medium text-gray-900">
          Your Music Library ({songs.length} songs)
        </h2>
      </div>
      
      <div className="divide-y divide-gray-200">
        {songs.map((song) => (
          <div key={song.id} className="p-6 hover:bg-gray-50">
            {editingSong === song.id ? (
              // Edit mode
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input
                    type="text"
                    value={editForm.title || ''}
                    onChange={(e) => handleEditChange('title', e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="Title"
                  />
                  <input
                    type="text"
                    value={editForm.artist || ''}
                    onChange={(e) => handleEditChange('artist', e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="Artist"
                  />
                  <input
                    type="text"
                    value={editForm.album || ''}
                    onChange={(e) => handleEditChange('album', e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="Album"
                  />
                  <input
                    type="text"
                    value={editForm.genre || ''}
                    onChange={(e) => handleEditChange('genre', e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="Genre"
                  />
                </div>
                <div className="flex justify-end space-x-3">
                  <button
                    onClick={handleCancelEdit}
                    className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSaveEdit}
                    className="px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-md hover:bg-primary-700"
                  >
                    Save
                  </button>
                </div>
              </div>
            ) : (
              // Display mode
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-4">
                  {song.artwork_url ? (
                    <img
                      src={song.artwork_url}
                      alt={`${song.title} artwork`}
                      className="w-16 h-16 rounded-lg object-cover flex-shrink-0"
                      onError={(e) => {
                        e.target.style.display = 'none';
                      }}
                    />
                  ) : (
                    <div className="w-16 h-16 rounded-lg bg-gray-200 flex items-center justify-center flex-shrink-0">
                      <span className="text-2xl">🎵</span>
                    </div>
                  )}
                  
                  <div className="flex-1 min-w-0">
                    <h3 className="text-lg font-medium text-gray-900 truncate">
                      {song.title}
                    </h3>
                    <p className="text-sm text-gray-600">by {song.artist}</p>
                    
                    <div className="mt-2 space-y-1">
                      {song.album && (
                        <p className="text-sm text-gray-500">
                          <span className="font-medium">Album:</span> {song.album}
                        </p>
                      )}
                      {song.genre && (
                        <p className="text-sm text-gray-500">
                          <span className="font-medium">Genre:</span> {song.genre}
                        </p>
                      )}
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        {song.year && <span>{song.year}</span>}
                        {song.duration && <span>{formatDuration(song.duration)}</span>}
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2 flex-shrink-0">
                  <button
                    onClick={() => handleEdit(song)}
                    className="p-2 text-gray-400 hover:text-primary-600 rounded-full hover:bg-gray-100"
                    title="Edit song"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button
                    onClick={() => onDelete(song.id)}
                    className="p-2 text-gray-400 hover:text-red-600 rounded-full hover:bg-gray-100"
                    title="Delete song"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default SongList;
