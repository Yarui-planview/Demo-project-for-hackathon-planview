import React from 'react';
import { Song } from '../types';
import SongCard from './SongCard';

interface MusicLibraryProps {
  songs: Song[];
  onDelete: (id: string) => void;
}

const MusicLibrary: React.FC<MusicLibraryProps> = ({ songs, onDelete }) => {
  if (songs.length === 0) {
    return (
      <div className="music-library empty">
        <div className="empty-state">
          <h2>🎵 No songs in your library</h2>
          <p>Add your first song to get started!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="music-library">
      <h2>Your Music Library ({songs.length} songs)</h2>
      <div className="songs-grid">
        {songs.map(song => (
          <SongCard 
            key={song.id} 
            song={song} 
            onDelete={onDelete}
          />
        ))}
      </div>
    </div>
  );
};

export default MusicLibrary;