# Music Library 🎵

A full-stack serverless web application for managing your personal music collection. Built with React frontend and Python backend.

![Music Library Interface](https://github.com/user-attachments/assets/ae653d28-3244-421e-9d5a-23350dae6b1e)

## Features

- ✨ **Modern React Frontend**: Beautiful, responsive UI with TypeScript
- 🐍 **Python Flask Backend**: RESTful API for music data management
- 🔍 **Search Functionality**: Find songs by title, artist, album, or genre
- 📊 **Library Statistics**: View counts of songs, artists, albums, and genres
- ➕ **Add New Songs**: Easy form to add songs with validation
- 🗑️ **Delete Songs**: Remove songs from your collection
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 💾 **Data Persistence**: Songs are saved to local JSON file

## Screenshots

### Main Library View
![Music Library with Songs](https://github.com/user-attachments/assets/0e4d203e-1610-4ccd-a7fa-a70966d9145d)

*The main interface showing your music collection with search and statistics*

## Tech Stack

### Frontend
- **React 18** with TypeScript
- **Modern CSS** with CSS Variables and Grid Layout
- **Axios** for API communication
- **Responsive Design** for all screen sizes

### Backend
- **Flask** - Python web framework
- **Flask-CORS** - Cross-origin resource sharing
- **JSON** - Data storage (easily replaceable with database)
- **RESTful API** design

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/songs` | Get all songs |
| POST | `/api/songs` | Add new song |
| GET | `/api/songs/{id}` | Get specific song |
| PUT | `/api/songs/{id}` | Update song |
| DELETE | `/api/songs/{id}` | Delete song |
| GET | `/api/songs/search?q={query}` | Search songs |
| GET | `/api/stats` | Get library statistics |

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask server:
   ```bash
   python app.py
   ```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will run on `http://localhost:3000`

### Testing

Test the backend API:
```bash
cd backend
source venv/bin/activate
pip install requests
python test_api.py
```

## Project Structure

```
.
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── test_api.py        # API test script
│   └── music_data.json    # Data storage (auto-generated)
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/      # API service layer
│   │   ├── types.ts       # TypeScript interfaces
│   │   ├── App.tsx        # Main App component
│   │   └── App.css        # Styling
│   ├── public/
│   └── package.json
└── README.md
```

## Usage

1. **Adding Songs**: Click "Add New Song" and fill in the required fields (Title, Artist, Album) and optional fields (Genre, Year, Duration)

2. **Searching**: Use the search bar to find songs by any field - title, artist, album, or genre

3. **Viewing Statistics**: The dashboard shows your library statistics including total counts

4. **Deleting Songs**: Click the trash icon on any song card to remove it from your library

## Development

### Backend API Testing
The backend includes a test script (`test_api.py`) that demonstrates all API endpoints:
```bash
cd backend
python test_api.py
```

### Frontend Development
The React app uses modern hooks and TypeScript for type safety. Components are organized by feature:

- `MusicLibrary` - Main library display
- `SongCard` - Individual song display
- `AddSong` - Add new song form
- `SearchBar` - Search functionality
- `Stats` - Library statistics

## Deployment

### Production Considerations

For production deployment:

1. **Backend**: Use a production WSGI server like Gunicorn
2. **Database**: Replace JSON storage with PostgreSQL/MongoDB
3. **Environment Variables**: Use `.env` files for configuration
4. **CORS**: Configure proper CORS settings for your domain
5. **SSL**: Enable HTTPS for secure communication

### Serverless Deployment Options

This application is designed for serverless deployment:

- **Frontend**: Deploy to Vercel, Netlify, or AWS S3 + CloudFront
- **Backend**: Deploy to AWS Lambda, Google Cloud Functions, or Vercel Functions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details