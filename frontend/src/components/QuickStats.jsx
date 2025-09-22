import React from 'react';

const QuickStats = ({ songs }) => {
  const totalDuration = songs.reduce((sum, song) => sum + (song.duration || 0), 0);
  const genres = [...new Set(songs.filter(song => song.genre).map(song => song.genre))];
  const averageYear = songs.filter(song => song.year).length > 0 
    ? Math.round(songs.filter(song => song.year).reduce((sum, song) => sum + song.year, 0) / songs.filter(song => song.year).length)
    : 0;

  const formatTotalDuration = (seconds) => {
    if (!seconds) return '0:00';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 mb-8">
      <h3 className="text-lg font-medium text-gray-900 mb-4">📊 Quick Stats</h3>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="text-center">
          <div className="text-2xl font-bold text-primary-600">{totalDuration ? formatTotalDuration(totalDuration) : '0:00'}</div>
          <div className="text-sm text-gray-500">Total Playtime</div>
        </div>
        
        <div className="text-center">
          <div className="text-2xl font-bold text-green-600">{genres.length}</div>
          <div className="text-sm text-gray-500">Genres</div>
        </div>
        
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600">{averageYear || 'N/A'}</div>
          <div className="text-sm text-gray-500">Avg Year</div>
        </div>
        
        <div className="text-center">
          <div className="text-2xl font-bold text-purple-600">
            {songs.length > 0 ? Math.round(totalDuration / songs.length) || 0 : 0}s
          </div>
          <div className="text-sm text-gray-500">Avg Duration</div>
        </div>
      </div>

      {genres.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Genres in your library:</h4>
          <div className="flex flex-wrap gap-2">
            {genres.slice(0, 10).map((genre, index) => (
              <span
                key={index}
                className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
              >
                {genre}
              </span>
            ))}
            {genres.length > 10 && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-200 text-gray-600">
                +{genres.length - 10} more
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default QuickStats;
