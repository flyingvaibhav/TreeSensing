# TreeSense - Quick Start Script

Write-Host "🌳 TreeSense Tree Detection Service" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""

# Check if MongoDB is needed
Write-Host "⚠️  Make sure MongoDB is running!" -ForegroundColor Yellow
Write-Host ""

# Backend setup
Write-Host "📦 Setting up Backend..." -ForegroundColor Cyan
Set-Location -Path "$PSScriptRoot\backend"

if (!(Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    "MONGO_URI=mongodb://localhost:27017" | Out-File -FilePath ".env" -Encoding utf8
}

Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "✅ Backend setup complete!" -ForegroundColor Green
Write-Host ""

# Frontend setup
Write-Host "📦 Setting up Frontend..." -ForegroundColor Cyan
Set-Location -Path "$PSScriptRoot\frontend"

if (!(Test-Path ".env.local")) {
    Write-Host "Creating .env.local file..." -ForegroundColor Yellow
    "NEXT_PUBLIC_API_URL=http://127.0.0.1:8000" | Out-File -FilePath ".env.local" -Encoding utf8
}

Write-Host "Installing Node dependencies..." -ForegroundColor Yellow
pnpm install

Write-Host ""
Write-Host "✅ Frontend setup complete!" -ForegroundColor Green
Write-Host ""

# Instructions
Write-Host "🚀 To start the services:" -ForegroundColor Green
Write-Host ""
Write-Host "Backend (in backend folder):" -ForegroundColor Cyan
Write-Host "  uvicorn main:app --reload" -ForegroundColor White
Write-Host ""
Write-Host "Frontend (in frontend folder):" -ForegroundColor Cyan
Write-Host "  pnpm dev" -ForegroundColor White
Write-Host ""
Write-Host "Then open: http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
