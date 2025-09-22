# Music Library - Full Stack Serverless Web Application

A personal music collection management system built with React frontend and Python backend.

## Features

- 🎵 Add, edit, and delete songs from your music library
- 🎨 View album artwork and song details
- 🔍 Search and filter your music collection
- 📱 Responsive design for desktop and mobile
- ☁️ Serverless architecture for scalability

## Tech Stack

### Frontend
- **React** - Modern UI library
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls

### Backend
- **Python** - Backend language
- **FastAPI** - Modern web framework for APIs
- **SQLite** - Lightweight database
- **Pydantic** - Data validation

## Project Structure

```
music-library/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API service functions
│   │   └── utils/           # Utility functions
│   ├── public/              # Static assets
│   └── package.json         # Frontend dependencies
├── backend/                 # Python backend application
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── routes/          # API route handlers
│   │   ├── services/        # Business logic
│   │   └── main.py          # FastAPI application entry point
│   ├── requirements.txt     # Python dependencies
│   └── database.db          # SQLite database
└── README.md               # Project documentation
```

## Getting Started

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- Git

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```

The backend API will be available at http://localhost:8000

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
npm run dev
```

The frontend will be available at http://localhost:5173

## API Endpoints

- `GET /api/songs` - Get all songs
- `POST /api/songs` - Add a new song
- `GET /api/songs/{id}` - Get a specific song
- `PUT /api/songs/{id}` - Update a song
- `DELETE /api/songs/{id}` - Delete a song
- `GET /api/search?q={query}` - Search songs

## Development

1. Start the backend server on port 8000
2. Start the frontend development server on port 5173
3. The frontend is configured to proxy API requests to the backend

## Deployment

This application is designed to be deployed as a serverless application:
- Frontend can be deployed to Vercel, Netlify, or similar
- Backend can be deployed to AWS Lambda, Google Cloud Functions, or similar

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License