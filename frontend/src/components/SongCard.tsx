import React from 'react';
import { Song } from '../types';

interface SongCardProps {
  song: Song;
  onDelete: (id: string) => void;
}

const SongCard: React.FC<SongCardProps> = ({ song, onDelete }) => {
  const handleDelete = () => {
    if (window.confirm(`Are you sure you want to delete "${song.title}" by ${song.artist}?`)) {
      onDelete(song.id);
    }
  };

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString();
    } catch {
      return dateString;
    }
  };

  return (
    <div className="song-card">
      <div className="song-header">
        <h3 className="song-title">{song.title}</h3>
        <button 
          className="delete-btn"
          onClick={handleDelete}
          title="Delete song"
        >
          🗑️
        </button>
      </div>
      
      <div className="song-details">
        <p className="artist">
          <strong>Artist:</strong> {song.artist}
        </p>
        <p className="album">
          <strong>Album:</strong> {song.album}
        </p>
        
        {song.genre && (
          <p className="genre">
            <strong>Genre:</strong> {song.genre}
          </p>
        )}
        
        {song.year && (
          <p className="year">
            <strong>Year:</strong> {song.year}
          </p>
        )}
        
        {song.duration && (
          <p className="duration">
            <strong>Duration:</strong> {song.duration}
          </p>
        )}
      </div>
      
      <div className="song-footer">
        <span className="date-added">
          Added: {formatDate(song.date_added)}
        </span>
      </div>
    </div>
  );
};

export default SongCard;