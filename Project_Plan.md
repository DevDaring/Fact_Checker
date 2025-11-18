# Fact Checker - Complete Execution Plan

## 🎯 Project Overview
A web application for fact-checking multimedia content (video, audio, image) using Google Cloud services and Gemini 2.5 Flash with Search Grounding.

------------
Description - Root folder will contain .env with all API keys and json file location.
Json file will be used for google speech to text and text speech service.
This json file is downloaded for GCP service account.
frontend folder will contain all frontend files in React+TS+Vite
backend folder will contain all python files with fastapi for api
Database will csv and folders for storing images. This will be stored in Data folder in root.

Here is the idea-
Name- Fact Checker
Tagline - Let's Make Difference Between Fact and Illusion
User will login to application with mail id and password. In a dropdown, user will select 'User'.
User can upload Video, Audio or image.
From video the application will take audio and send it to google speech to text
From audio it will directly send it to speech to text service.
After it is converted to text, it will be sent to gemini 2.5 flash with Google Search Grounding.
Uploaded image will also be sent to gemini 2.5 flash with Google Search Grounding.
Keys from AI studio will be given to .env.
Application will return the fact with evidence and citation link.
That will be shown on UI.
These search will be saved in user history.
Admin will have different login and password credential. In drop down admin will select 'Admin' so he can login and can see all user data.
Admin can not modify but comment on that data. This comment user can see.
---

## 📋 Execution Plan

### **Phase 1: Setup & Configuration (Day 1)**
1. Initialize project structure
2. Set up Python virtual environment
3. Create React + TypeScript + Vite frontend
4. Configure .env file with all API keys
5. Set up GCP service account and download JSON credentials
6. Initialize CSV database structure

### **Phase 2: Backend Development (Day 1-2)**
1. Build FastAPI server with CORS configuration
2. Implement authentication system (User/Admin)
3. Create file upload endpoints (video, audio, image)
4. Integrate Google Speech-to-Text API
5. Integrate Gemini 2.5 Flash API with Search Grounding
6. Implement video audio extraction logic
7. Build history management system
8. Create admin commenting functionality

### **Phase 3: Frontend Development (Day 2-3)**
1. Design login page with role dropdown
2. Create file upload interface
3. Build results display component with citations
4. Implement user history view
5. Develop admin dashboard
6. Add loading states and error handling

### **Phase 4: Integration & Testing (Day 3)**
1. Connect frontend to backend APIs
2. Test all upload types (video, audio, image)
3. Verify fact-checking pipeline
4. Test user/admin workflows
5. Handle edge cases and errors

### **Phase 5: Polish & Deployment (Day 3-4)**
1. UI/UX improvements
2. Add responsive design
3. Optimize performance
4. Prepare demo presentation
5. Create README and documentation

---

## 📁 Complete Folder Structure

```
fact-checker/
│
├── .env                          # Environment variables (API keys)
├── gcp-credentials.json          # Google Cloud service account JSON
├── requirements.txt              # Python dependencies
├── package.json                  # Root package.json for scripts
├── README.md                     # Project documentation
├── .gitignore                    # Git ignore file
│
├── Data/                         # Database and media storage
│   ├── users.csv                 # User credentials and metadata
│   ├── fact_checks.csv          # All fact-check records
│   ├── admin_comments.csv       # Admin comments on fact-checks
│   ├── uploads/                 # Uploaded files
│   │   ├── videos/              # Video files
│   │   ├── audio/               # Audio files
│   │   └── images/              # Image files
│   └── temp/                    # Temporary files (audio extraction)
│
├── backend/                      # FastAPI backend
│   ├── main.py                  # FastAPI application entry point
│   ├── requirements.txt         # Backend-specific dependencies
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # Load environment variables and configuration
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # User data model (Pydantic)
│   │   ├── fact_check.py        # Fact check data model
│   │   └── comment.py           # Admin comment data model
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py              # Login/logout endpoints
│   │   ├── upload.py            # File upload endpoints
│   │   ├── fact_check.py        # Fact-checking endpoints
│   │   ├── history.py           # User history endpoints
│   │   └── admin.py             # Admin-specific endpoints
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py      # Authentication logic
│   │   ├── speech_to_text.py   # Google Speech-to-Text integration
│   │   ├── gemini_service.py   # Gemini 2.5 Flash API integration
│   │   ├── video_processor.py  # Video audio extraction (ffmpeg)
│   │   ├── file_handler.py     # File upload/storage management
│   │   └── database.py          # CSV database operations
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py        # Input validation utilities
│   │   └── helpers.py           # General helper functions
│   │
│   └── middleware/
│       ├── __init__.py
│       └── auth_middleware.py   # JWT token verification
│
└── frontend/                     # React + TypeScript + Vite
    ├── index.html               # HTML entry point
    ├── package.json             # Frontend dependencies
    ├── tsconfig.json            # TypeScript configuration
    ├── vite.config.ts           # Vite configuration
    ├── .env.local               # Frontend environment variables
    │
    ├── public/
    │   ├── favicon.ico          # App favicon
    │   └── logo.png             # App logo
    │
    └── src/
        ├── main.tsx             # Application entry point
        ├── App.tsx              # Main App component with routing
        ├── vite-env.d.ts        # Vite type declarations
        │
        ├── assets/              # Static assets
        │   ├── images/
        │   └── styles/
        │       └── global.css   # Global styles
        │
        ├── components/          # Reusable components
        │   ├── Navbar.tsx       # Navigation bar
        │   ├── FileUpload.tsx   # File upload component
        │   ├── ResultCard.tsx   # Fact-check result display
        │   ├── HistoryItem.tsx  # History list item
        │   ├── CommentBox.tsx   # Admin comment component
        │   └── LoadingSpinner.tsx # Loading indicator
        │
        ├── pages/               # Page components
        │   ├── Login.tsx        # Login page with role dropdown
        │   ├── UserDashboard.tsx # User main interface
        │   ├── AdminDashboard.tsx # Admin interface
        │   ├── HistoryPage.tsx  # User history view
        │   └── NotFound.tsx     # 404 page
        │
        ├── context/             # React Context
        │   └── AuthContext.tsx  # Authentication state management
        │
        ├── services/            # API service layer
        │   ├── api.ts           # Axios instance configuration
        │   ├── authService.ts   # Authentication API calls
        │   ├── uploadService.ts # File upload API calls
        │   ├── factCheckService.ts # Fact-check API calls
        │   └── adminService.ts  # Admin API calls
        │
        ├── types/               # TypeScript types/interfaces
        │   ├── user.ts          # User type definitions
        │   ├── factCheck.ts     # Fact check type definitions
        │   └── api.ts           # API response types
        │
        ├── utils/               # Utility functions
        │   ├── validators.ts    # Form validation
        │   └── formatters.ts    # Data formatting helpers
        │
        └── hooks/               # Custom React hooks
            ├── useAuth.ts       # Authentication hook
            └── useFileUpload.ts # File upload hook
```

---

## 📄 File Descriptions

### **Root Level Files**

**`.env`**
- Contains all API keys and configuration
- Variables: `GEMINI_API_KEY`, `GCP_PROJECT_ID`, `GCP_CREDENTIALS_PATH`, `JWT_SECRET_KEY`, `BACKEND_PORT`, `FRONTEND_PORT`

**`gcp-credentials.json`**
- Google Cloud Platform service account JSON file
- Used for Speech-to-Text and Text-to-Speech authentication

**`requirements.txt`**
- All Python dependencies for the project
- Includes: fastapi, uvicorn, google-cloud-speech, google-generativeai, python-multipart, pandas, pydantic, python-jose, passlib, python-dotenv, ffmpeg-python

**`README.md`**
- Project overview, setup instructions, API documentation, and usage guide

---

### **Data Folder**

**`users.csv`**
- Columns: `user_id`, `email`, `password_hash`, `role` (User/Admin), `created_at`, `last_login`
- Stores user credentials and metadata

**`fact_checks.csv`**
- Columns: `fact_check_id`, `user_id`, `upload_type` (video/audio/image), `file_path`, `extracted_text`, `gemini_response`, `citations`, `timestamp`
- Stores all fact-check history

**`admin_comments.csv`**
- Columns: `comment_id`, `fact_check_id`, `admin_id`, `comment_text`, `timestamp`
- Stores admin comments on user fact-checks

**`uploads/` subdirectories**
- Organized storage for uploaded media files by type
- Files named with timestamp + user_id for uniqueness

---

### **Backend Files**

**`main.py`**
- FastAPI app initialization
- CORS middleware configuration
- Route registration
- Server startup configuration

**`config/settings.py`**
- Loads environment variables from .env
- Defines application configuration constants
- GCP credentials path setup

**`models/user.py`**
- Pydantic models for user data
- `UserCreate`, `UserLogin`, `UserResponse` schemas

**`models/fact_check.py`**
- Pydantic models for fact-check data
- `FactCheckRequest`, `FactCheckResponse`, `FactCheckHistory` schemas

**`models/comment.py`**
- Pydantic models for admin comments
- `CommentCreate`, `CommentResponse` schemas

**`routes/auth.py`**
- `/api/auth/login` - User/Admin login with role selection
- `/api/auth/logout` - Logout endpoint
- `/api/auth/register` - User registration (optional)

**`routes/upload.py`**
- `/api/upload/video` - Video file upload
- `/api/upload/audio` - Audio file upload
- `/api/upload/image` - Image file upload
- Handles file validation and storage

**`routes/fact_check.py`**
- `/api/fact-check/process` - Main fact-checking endpoint
- Processes uploaded files through the pipeline
- Returns fact-checked results with citations

**`routes/history.py`**
- `/api/history/user/{user_id}` - Get user fact-check history
- `/api/history/details/{fact_check_id}` - Get specific fact-check details

**`routes/admin.py`**
- `/api/admin/all-users` - Get all users data
- `/api/admin/user-checks/{user_id}` - Get specific user's fact-checks
- `/api/admin/comment` - Add comment to fact-check
- `/api/admin/comments/{fact_check_id}` - Get comments for fact-check

**`services/auth_service.py`**
- JWT token generation and verification
- Password hashing and validation
- User authentication logic
- Role-based access control

**`services/speech_to_text.py`**
- Google Speech-to-Text API integration
- Audio file transcription
- Language detection
- Error handling for transcription failures

**`services/gemini_service.py`**
- Gemini 2.5 Flash API integration with Search Grounding
- Text-based fact-checking
- Image-based fact-checking
- Citation extraction from responses

**`services/video_processor.py`**
- Extract audio from video files using ffmpeg
- Convert to compatible audio format for Speech-to-Text
- Temporary file management

**`services/file_handler.py`**
- File upload validation (size, type)
- Save files to appropriate folders
- Generate unique filenames
- File cleanup utilities

**`services/database.py`**
- CSV read/write operations
- User CRUD operations
- Fact-check record management
- Comment management
- Data validation and error handling

**`utils/validators.py`**
- Email validation
- Password strength validation
- File type validation
- Input sanitization

**`middleware/auth_middleware.py`**
- JWT token verification middleware
- Protected route decorator
- Role-based access control middleware

---

### **Frontend Files**

**`src/main.tsx`**
- React application entry point
- Renders App component
- React Router setup

**`src/App.tsx`**
- Main application component
- Route configuration (Login, UserDashboard, AdminDashboard, History)
- AuthContext provider wrapper
- Protected route logic

**`vite.config.ts`**
- Vite build configuration
- Proxy setup for backend API calls
- Plugin configuration

**`tsconfig.json`**
- TypeScript compiler configuration
- Path aliases
- Type checking rules

**`src/components/Navbar.tsx`**
- Navigation bar with user info
- Logout button
- Role display (User/Admin)

**`src/components/FileUpload.tsx`**
- Drag-and-drop file upload interface
- File type selection (video/audio/image)
- Upload progress indicator
- File preview

**`src/components/ResultCard.tsx`**
- Display fact-check results
- Show Gemini response
- Display citations as clickable links
- Show evidence sources

**`src/components/HistoryItem.tsx`**
- Individual history record display
- Timestamp formatting
- Click to view details
- Admin comment indicator

**`src/components/CommentBox.tsx`**
- Admin comment input form
- Comment display for users
- Timestamp formatting

**`src/components/LoadingSpinner.tsx`**
- Loading animation
- Processing status messages

**`src/pages/Login.tsx`**
- Email and password input fields
- Role dropdown (User/Admin)
- Form validation
- Error message display

**`src/pages/UserDashboard.tsx`**
- File upload section
- Recent fact-checks display
- Navigation to history page
- Result display area

**`src/pages/AdminDashboard.tsx`**
- All users list
- Search/filter users
- View user fact-checks
- Add comments interface

**`src/pages/HistoryPage.tsx`**
- Paginated history list
- Filter by date/type
- Click to view details
- Admin comments display

**`src/context/AuthContext.tsx`**
- User authentication state
- Login/logout functions
- Role management
- Protected route logic

**`src/services/api.ts`**
- Axios instance with base URL
- Request/response interceptors
- JWT token attachment
- Error handling

**`src/services/authService.ts`**
- `login(email, password, role)` - Login API call
- `logout()` - Logout API call
- `getCurrentUser()` - Get current user info

**`src/services/uploadService.ts`**
- `uploadVideo(file)` - Upload video
- `uploadAudio(file)` - Upload audio
- `uploadImage(file)` - Upload image
- Progress tracking

**`src/services/factCheckService.ts`**
- `processFactCheck(fileId, type)` - Process uploaded file
- `getHistory(userId)` - Get user history
- `getDetails(factCheckId)` - Get fact-check details

**`src/services/adminService.ts`**
- `getAllUsers()` - Get all users
- `getUserChecks(userId)` - Get user's fact-checks
- `addComment(factCheckId, comment)` - Add comment

**`src/types/user.ts`**
- `User` interface
- `LoginRequest` interface
- `AuthResponse` interface

**`src/types/factCheck.ts`**
- `FactCheck` interface
- `FactCheckResult` interface
- `Citation` interface

**`src/hooks/useAuth.ts`**
- Custom hook for authentication
- Returns current user, login, logout functions
- Role checking utilities

**`src/hooks/useFileUpload.ts`**
- Custom hook for file uploads
- Upload progress state
- Error handling
- Success callbacks

---

## 🔑 Key Technologies

**Backend:**
- FastAPI (REST API)
- Google Cloud Speech-to-Text
- Gemini 2.5 Flash with Search Grounding
- FFmpeg (video audio extraction)
- JWT authentication
- Pandas (CSV operations)

**Frontend:**
- React 18
- TypeScript
- Vite
- Axios
- React Router
- Context API

**Storage:**
- CSV files (database)
- Local file system (media storage)

---

## 🚀 Deployment Checklist

1. ✅ Set up all API keys in .env
2. ✅ Download GCP service account JSON
3. ✅ Install Python dependencies
4. ✅ Install Node dependencies
5. ✅ Create initial admin user in users.csv
6. ✅ Test all upload types
7. ✅ Test fact-checking pipeline
8. ✅ Test admin functionality
9. ✅ Deploy backend (FastAPI server)
10. ✅ Deploy frontend (Vite build)

---

## 📊 Success Metrics

- User can upload and fact-check files in <30 seconds
- Admin can view all data and add comments
- Citations are clickable and accurate
- History is properly maintained
- No data loss between sessions

**This plan provides a complete roadmap for your hackathon project. Good luck! 🎉**
