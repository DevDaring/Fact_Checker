# Reload PATH to include ffmpeg and other newly installed programs
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Start the FastAPI server
Write-Host "Starting Fact Checker Backend Server..."
Write-Host "FFmpeg location: $(where.exe ffmpeg)"
python main.py
