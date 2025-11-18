# Fact Checker

**Tagline:** *Let's Make Difference Between Fact and Fiction*

A comprehensive web application for fact-checking multimedia content (video, audio, image) using Google Cloud Services and Gemini 2.5 Flash with Search Grounding.

## 🎯 Features

- **Multi-format Support**: Upload and analyze videos, audio files, and images
- **Speech-to-Text**: Automatic audio extraction from videos and transcription using Google Cloud Speech-to-Text
- **AI-Powered Fact-Checking**: Leverages Gemini 2.5 Flash with Google Search Grounding for accurate verification
- **Citation & Evidence**: Displays sources and citations for fact-check results
- **User History**: Track all your past fact-checks with admin comments
- **Admin Dashboard**: Complete oversight of all users and fact-checks with commenting functionality
- **Role-Based Access**: Separate user and admin interfaces

## 📁 Project Structure

```
fact-checker/
├── .env                          # Environment variables
├── gcp-credentials.json          # Google Cloud credentials (not included)
├── package.json                  # Root package scripts
├── README.md                     # This file
├── Project_Plan.md               # Detailed project plan
│
├── Data/                         # CSV database and uploads
│   ├── users.csv
│   ├── fact_checks.csv
│   ├── admin_comments.csv
│   └── uploads/
│       ├── videos/
│       ├── audio/
│       └── images/
│
├── backend/                      # FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   ├── config/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   └── middleware/
│
└── frontend/                     # React + TypeScript + Vite
    ├── index.html
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── components/
        ├── pages/
        ├── context/
        ├── services/
        ├── types/
        ├── utils/
        └── hooks/
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 18+**
- **FFmpeg** (for video processing)
- **Google Cloud Account** with Speech-to-Text API enabled
- **Gemini API Key** from Google AI Studio

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Fact_Checker
   ```

2. **Set up environment variables**

   Copy the `.env` file and fill in your API keys:
   ```bash
   # Edit .env file with your credentials
   GEMINI_API_KEY=your_gemini_api_key_here
   GCP_PROJECT_ID=your_gcp_project_id
   GCP_CREDENTIALS_PATH=./gcp-credentials.json
   JWT_SECRET_KEY=your_secret_key_here
   ```

3. **Download GCP Service Account JSON**
   - Go to Google Cloud Console
   - Create a service account with Speech-to-Text API access
   - Download the JSON key file
   - Save it as `gcp-credentials.json` in the root directory

4. **Install dependencies**
   ```bash
   # Install backend dependencies
   cd backend
   pip install -r requirements.txt

   # Install frontend dependencies
   cd ../frontend
   npm install

   # Or install all at once from root
   cd ..
   npm install
   npm run install:all
   ```

5. **Install FFmpeg** (Required for video/audio processing)

   **Windows:**
   1. Download FFmpeg from https://www.gyan.dev/ffmpeg/builds/ (get the full build)
   2. Extract the ZIP file to `C:\ffmpeg`
   3. Add FFmpeg to your system PATH:
      - Press `Win + X` and select "System"
      - Click "Advanced system settings"
      - Click "Environment Variables"
      - Under "System Variables", find and edit "Path"
      - Click "New" and add `C:\ffmpeg\bin`
      - Click OK on all windows
   4. Restart your terminal/IDE
   5. Verify installation: `ffmpeg -version`

   **Alternative (Windows with Chocolatey):**
   ```bash
   choco install ffmpeg
   ```

   **macOS:**
   ```bash
   brew install ffmpeg
   ```

   **Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install ffmpeg
   ```

   **Fedora:**
   ```bash
   sudo dnf install ffmpeg
   ```

### Running the Application

#### Development Mode

**Option 1: Run both servers concurrently (recommended)**
```bash
npm run dev
```

**Option 2: Run servers separately**
```bash
# Terminal 1 - Backend
npm run dev:backend
# or
cd backend && python main.py

# Terminal 2 - Frontend
npm run dev:frontend
# or
cd frontend && npm run dev
```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs

#### Production Mode

```bash
# Build frontend
npm run build:frontend

# Start backend
npm run start:backend

# Start frontend preview
npm run start:frontend
```

## 👤 User Accounts

### Default Admin Account
- **Email**: admin@factchecker.com
- **Password**: admin123
- **Role**: Admin

### Creating New Users
Users can register through the login page or be added directly to `Data/users.csv`.

## 📖 Usage Guide

### For Users

1. **Login**
   - Navigate to http://localhost:5173
   - Enter your email and password
   - Select "User" role
   - Click Login

2. **Upload Content**
   - Select content type (Video, Audio, or Image)
   - Drag & drop or browse to select file
   - Click "Upload and Fact Check"

3. **View Results**
   - See extracted text (for video/audio)
   - Read AI-powered fact-check analysis
   - Explore citations and sources
   - View admin comments if available

4. **Check History**
   - Navigate to History page
   - View all past fact-checks
   - Click on any item to see full details

### For Admins

1. **Login as Admin**
   - Use admin credentials
   - Select "Admin" role

2. **View All Users**
   - See all registered users
   - Click on a user to view their fact-checks

3. **Review Fact-Checks**
   - Browse through user submissions
   - Read detailed analysis and results

4. **Add Comments**
   - Open any fact-check
   - Add administrative comments
   - Users can see these comments in their history

## 🔧 Configuration

### Backend Configuration (.env)

```env
# API Keys
GEMINI_API_KEY=your_key_here
GCP_PROJECT_ID=your_project_id
GCP_CREDENTIALS_PATH=./gcp-credentials.json

# JWT Settings
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Server Ports
BACKEND_PORT=8000
FRONTEND_PORT=5173

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# File Upload Limits
MAX_FILE_SIZE_MB=100
```

### Frontend Configuration (frontend/.env.local)

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Google Cloud Speech-to-Text**: Audio transcription
- **Gemini 2.5 Flash**: AI-powered fact-checking with Search Grounding
- **FFmpeg**: Video/audio processing
- **Pandas**: CSV database operations
- **JWT**: Authentication

### Frontend
- **React 18**: UI framework
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool
- **React Router**: Navigation
- **Axios**: HTTP client
- **Context API**: State management

### Storage
- **CSV Files**: Lightweight database
- **Local File System**: Media storage

## 📚 API Documentation

Once the backend is running, visit http://localhost:8000/api/docs for interactive API documentation (Swagger UI).

### Key Endpoints

#### Authentication
- `POST /api/auth/login` - User/Admin login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - Logout

#### File Upload
- `POST /api/upload/video` - Upload video file
- `POST /api/upload/audio` - Upload audio file
- `POST /api/upload/image` - Upload image file

#### Fact-Checking
- `POST /api/fact-check/process` - Process uploaded file
- `GET /api/fact-check/result/{id}` - Get fact-check result

#### History
- `GET /api/history/user` - Get current user's history
- `GET /api/history/details/{id}` - Get specific fact-check details

#### Admin
- `GET /api/admin/users` - Get all users (admin only)
- `GET /api/admin/fact-checks` - Get all fact-checks (admin only)
- `POST /api/admin/comment` - Add comment to fact-check
- `GET /api/admin/comments/{id}` - Get comments for fact-check

## 🔒 Security

- JWT-based authentication
- Role-based access control
- Password hashing with bcrypt
- File upload validation
- CORS protection
- Input sanitization

## 🐛 Troubleshooting

### Common Issues

1. **FFmpeg not found / WinError 2 / "The system cannot find the file specified"**

   This error occurs when FFmpeg is not installed or not in your system PATH.

   **Solution:**
   - Install FFmpeg following the detailed instructions in the Installation section above
   - On Windows, make sure to add FFmpeg's `bin` folder to your system PATH
   - **Important:** After adding to PATH, restart your terminal/IDE completely
   - Verify installation by running: `ffmpeg -version` in a new terminal
   - If you still see the error after installation, ensure you restarted your IDE/terminal

   **Quick Windows Fix:**
   ```bash
   # Using Chocolatey (easiest method)
   choco install ffmpeg

   # Then restart your terminal/IDE
   ```

2. **GCP Authentication Error**
   - Ensure `gcp-credentials.json` is in the root directory
   - Verify service account has Speech-to-Text API access
   - Check `GCP_CREDENTIALS_PATH` in `.env`

3. **Gemini API Error**
   - Verify `GEMINI_API_KEY` is correct
   - Check API quota and limits
   - Ensure you're using Gemini 2.0 Flash Exp or compatible model

4. **Port Already in Use**
   - Change ports in `.env` file
   - Kill existing processes using the ports

5. **CORS Errors**
   - Update `CORS_ORIGINS` in `.env`
   - Ensure frontend URL is in the allowed origins

## 📝 Development Notes

- CSV files serve as a simple database for development
- For production, consider migrating to PostgreSQL or MongoDB
- File uploads are stored locally; consider cloud storage for production
- Default admin password should be changed in production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

MIT License - feel free to use this project for learning and development.

## 👥 Support

For issues, questions, or suggestions:
- Check the API documentation at `/api/docs`
- Review `Project_Plan.md` for detailed architecture
- Open an issue on GitHub

## 🎉 Acknowledgments

- Google Cloud Platform for Speech-to-Text API
- Google AI Studio for Gemini API
- FastAPI and React communities
- All open-source contributors

---

**Built with ❤️ for truth and accuracy**
