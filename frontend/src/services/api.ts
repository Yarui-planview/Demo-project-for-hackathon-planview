import axios from 'axios';
import { Song, LibraryStats } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interfaces
interface SongsResponse {
  songs: Song[];
}

interface SongResponse {
  song: Song;
}

interface MessageResponse {
  message: string;
}

interface HealthResponse {
  status: string;
  message: string;
}

export const musicAPI = {
  async getSongs(): Promise<Song[]> {
    const response = await api.get<SongsResponse>('/songs');
    return response.data.songs;
  },

  async addSong(song: Omit<Song, 'id' | 'date_added'>): Promise<Song> {
    const response = await api.post<SongResponse>('/songs', song);
    return response.data.song;
  },

  async updateSong(id: string, song: Partial<Song>): Promise<Song> {
    const response = await api.put<SongResponse>(`/songs/${id}`, song);
    return response.data.song;
  },

  async deleteSong(id: string): Promise<void> {
    await api.delete<MessageResponse>(`/songs/${id}`);
  },

  async getSong(id: string): Promise<Song> {
    const response = await api.get<SongResponse>(`/songs/${id}`);
    return response.data.song;
  },

  async searchSongs(query: string): Promise<Song[]> {
    const response = await api.get<SongsResponse>(`/songs/search?q=${encodeURIComponent(query)}`);
    return response.data.songs;
  },

  async getStats(): Promise<LibraryStats> {
    const response = await api.get<LibraryStats>('/stats');
    return response.data;
  },

  async healthCheck(): Promise<{ status: string; message: string }> {
    const response = await api.get<HealthResponse>('/health');
    return response.data;
  }
};