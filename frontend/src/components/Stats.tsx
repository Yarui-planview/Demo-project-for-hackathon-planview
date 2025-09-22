import React from 'react';
import { LibraryStats } from '../types';

interface StatsProps {
  stats: LibraryStats;
}

const Stats: React.FC<StatsProps> = ({ stats }) => {
  return (
    <div className="library-stats">
      <div className="stats-grid">
        <div className="stat-item">
          <div className="stat-number">{stats.total_songs}</div>
          <div className="stat-label">Songs</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">{stats.total_artists}</div>
          <div className="stat-label">Artists</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">{stats.total_albums}</div>
          <div className="stat-label">Albums</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">{stats.total_genres}</div>
          <div className="stat-label">Genres</div>
        </div>
      </div>
    </div>
  );
};

export default Stats;