@echo off
start cmd /k "python backend/app.py"
timeout /t 2
start cmd /k "cd frontend_code && python -m http.server 8000"
echo Both servers are starting...
echo Flask backend will be available at http://localhost:5000
echo Frontend will be available at http://localhost:8000/index.html 