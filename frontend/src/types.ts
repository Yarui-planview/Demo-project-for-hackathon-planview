export interface Song {
  id: string;
  title: string;
  artist: string;
  album: string;
  genre?: string;
  year?: string;
  duration?: string;
  date_added: string;
}

export interface LibraryStats {
  total_songs: number;
  total_artists: number;
  total_albums: number;
  total_genres: number;
  artists: string[];
  genres: string[];
}