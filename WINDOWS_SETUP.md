# Windows Setup Guide for Fact Checker

This guide provides step-by-step instructions for setting up the Fact Checker application on Windows.

## Prerequisites Installation

### 1. Python 3.8+

1. Download Python from https://www.python.org/downloads/
2. **Important:** Check "Add Python to PATH" during installation
3. Verify installation:
   ```cmd
   python --version
   ```

### 2. Node.js 18+

1. Download Node.js from https://nodejs.org/
2. Install the LTS version
3. Verify installation:
   ```cmd
   node --version
   npm --version
   ```

### 3. FFmpeg (Critical for Video/Audio Processing)

**Method 1: Using Chocolatey (Recommended - Easiest)**

1. Install Chocolatey package manager:
   - Open PowerShell as Administrator
   - Run:
     ```powershell
     Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
     ```

2. Install FFmpeg:
   ```cmd
   choco install ffmpeg
   ```

3. Close and reopen your terminal

**Method 2: Manual Installation**

1. **Download FFmpeg:**
   - Go to https://www.gyan.dev/ffmpeg/builds/
   - Download "ffmpeg-release-full.7z" or "ffmpeg-release-full.zip"

2. **Extract FFmpeg:**
   - Extract the downloaded file to `C:\ffmpeg`
   - Your folder structure should look like:
     ```
     C:\ffmpeg\
     ├── bin\
     │   ├── ffmpeg.exe
     │   ├── ffplay.exe
     │   └── ffprobe.exe
     ├── doc\
     └── presets\
     ```

3. **Add to System PATH:**
   - Press `Win + X` and select "System"
   - Click "Advanced system settings" on the right
   - Click "Environment Variables" button
   - Under "System Variables", find and select "Path"
   - Click "Edit"
   - Click "New"
   - Add: `C:\ffmpeg\bin`
   - Click "OK" on all windows

4. **Verify Installation:**
   - **Important:** Close ALL terminal windows and your IDE
   - Open a NEW Command Prompt or PowerShell
   - Run:
     ```cmd
     ffmpeg -version
     ```
   - You should see FFmpeg version information

### 4. Git (Optional, for cloning)

1. Download from https://git-scm.com/download/win
2. Install with default options

## Project Setup

### 1. Clone or Download the Project

```cmd
git clone <repository-url>
cd Fact_Checker
```

Or download and extract the ZIP file.

### 2. Set Up Environment Variables

1. Copy the `.env` file in the root directory
2. Edit `.env` and add your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GCP_PROJECT_ID=your_gcp_project_id
GCP_CREDENTIALS_PATH=./gcp-credentials.json
JWT_SECRET_KEY=your_secret_key_here
```

### 3. Download GCP Credentials

1. Go to Google Cloud Console
2. Create or select a project
3. Enable Speech-to-Text API
4. Create a service account
5. Download the JSON key file
6. Save it as `gcp-credentials.json` in the project root

### 4. Install Python Dependencies

```cmd
cd backend
pip install -r requirements.txt
cd ..
```

### 5. Install Node.js Dependencies

```cmd
cd frontend
npm install
cd ..
```

## Running the Application

### Option 1: Run Both Servers (Recommended)

From the project root:

```cmd
npm install
npm run dev
```

### Option 2: Run Separately

**Terminal 1 - Backend:**
```cmd
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```cmd
cd frontend
npm run dev
```

## Accessing the Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs

## Common Windows Issues

### Issue 1: "FFmpeg not found" or "WinError 2"

**Symptoms:**
```
Error processing fact-check: Error extracting audio from video: [WinError 2] The system cannot find the file specified
```

**Solutions:**

1. **Verify FFmpeg is installed:**
   ```cmd
   ffmpeg -version
   ```

2. **If command not found:**
   - Follow the FFmpeg installation steps above
   - Make sure you added `C:\ffmpeg\bin` to PATH
   - **Restart your terminal/IDE completely**

3. **Check PATH:**
   ```cmd
   echo %PATH%
   ```
   - Should include `C:\ffmpeg\bin`

4. **If FFmpeg is installed but still not working:**
   - Close ALL terminal windows
   - Close your IDE/code editor
   - Reopen everything
   - Try again

### Issue 2: Python not found

**Solution:**
- Reinstall Python and check "Add Python to PATH"
- Or manually add to PATH: `C:\Python3X` and `C:\Python3X\Scripts`

### Issue 3: Port already in use

**Solution:**
```cmd
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

### Issue 4: Permission errors

**Solution:**
- Run Command Prompt or PowerShell as Administrator
- Or install dependencies in a virtual environment:

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue 5: SSL Certificate errors

**Solution:**
```cmd
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

## Development Tips for Windows

1. **Use PowerShell or Windows Terminal** instead of CMD for better experience

2. **Install Windows Terminal** from Microsoft Store for better terminal experience

3. **Use VS Code** with these extensions:
   - Python
   - Pylance
   - ESLint
   - TypeScript and JavaScript Language Features

4. **Create a virtual environment for Python:**
   ```cmd
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **If you have antivirus software**, add project folder to exclusions to avoid slow builds

## Testing the Setup

1. **Test Backend:**
   ```cmd
   cd backend
   python main.py
   ```
   - Should see: "FastAPI is starting..."
   - Visit: http://localhost:8000/docs

2. **Test Frontend:**
   ```cmd
   cd frontend
   npm run dev
   ```
   - Should see: "Local: http://localhost:5173"

3. **Test FFmpeg:**
   ```cmd
   ffmpeg -version
   ```
   - Should show version info

4. **Test Video Upload:**
   - Login to the app
   - Upload a small video file
   - Should process without errors

## Getting Help

If you encounter issues:

1. Check this guide's Common Issues section
2. Check the main README.md Troubleshooting section
3. Ensure all prerequisites are properly installed
4. Restart your terminal/IDE after PATH changes
5. Check backend logs in the terminal for detailed error messages

## Quick Troubleshooting Checklist

- [ ] Python installed and in PATH
- [ ] Node.js installed
- [ ] FFmpeg installed and in PATH
- [ ] All terminals/IDE restarted after PATH changes
- [ ] `.env` file configured with API keys
- [ ] `gcp-credentials.json` file in root directory
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Ports 8000 and 5173 are available
- [ ] Internet connection active (for API calls)

---

**For additional help, refer to the main README.md file.**
