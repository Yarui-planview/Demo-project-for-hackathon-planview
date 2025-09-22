import React, { useState } from 'react';

interface SearchBarProps {
  onSearch: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(query);
  };

  const handleClear = () => {
    setQuery('');
    onSearch('');
  };

  return (
    <div className="search-bar">
      <form onSubmit={handleSubmit}>
        <div className="search-input-group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by title, artist, album, or genre..."
            className="search-input"
          />
          <button type="submit" className="search-btn">
            🔍
          </button>
          {query && (
            <button 
              type="button" 
              className="clear-btn"
              onClick={handleClear}
            >
              ✖
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default SearchBar;