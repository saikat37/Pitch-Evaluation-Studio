# Installation & Testing Script for PowerShell
# Run this after creating your .env file with GROQ_API_KEY

Write-Host "🚀 Pitch Evaluation Studio - Setup Script" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python version
Write-Host "📌 Step 1: Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3\.([9]|1[0-9])") {
    Write-Host "✅ Python version OK: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python 3.9+ required. Found: $pythonVersion" -ForegroundColor Red
    exit 1
}

# Step 2: Check if .env exists
Write-Host ""
Write-Host "📌 Step 2: Checking .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✅ .env file found" -ForegroundColor Green
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "GROQ_API_KEY=.+") {
        Write-Host "✅ GROQ_API_KEY is set" -ForegroundColor Green
    } else {
        Write-Host "⚠️  GROQ_API_KEY not set in .env" -ForegroundColor Red
        Write-Host "   Please edit .env and add: GROQ_API_KEY=your_key_here" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "⚠️  .env file not found" -ForegroundColor Red
    Write-Host "   Creating .env from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "   Please edit .env and add your GROQ_API_KEY" -ForegroundColor Yellow
    exit 1
}

# Step 3: Create virtual environment
Write-Host ""
Write-Host "📌 Step 3: Setting up virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
} else {
    Write-Host "   Creating virtual environment..." -ForegroundColor Cyan
    python -m venv .venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Step 4: Activate and install dependencies
Write-Host ""
Write-Host "📌 Step 4: Installing dependencies..." -ForegroundColor Yellow
Write-Host "   This may take 3-5 minutes..." -ForegroundColor Cyan

& .\.venv\Scripts\Activate.ps1

Write-Host "   Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip --quiet

Write-Host "   Installing packages..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ All dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ Installation failed. Check errors above." -ForegroundColor Red
    exit 1
}

# Step 5: Quick import test
Write-Host ""
Write-Host "📌 Step 5: Testing imports..." -ForegroundColor Yellow
$testScript = @"
import streamlit
import langchain_groq
import langgraph
from faster_whisper import WhisperModel
import librosa
print("✅ All imports successful")
"@

$testScript | python 2>&1 | ForEach-Object {
    if ($_ -match "✅") {
        Write-Host $_ -ForegroundColor Green
    } elseif ($_ -match "Error|Traceback") {
        Write-Host $_ -ForegroundColor Red
    }
}

# Summary
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Make sure your virtual environment is activated:" -ForegroundColor White
Write-Host "      .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "   2. Run the app:" -ForegroundColor White
Write-Host "      streamlit run app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "   3. Open browser to: http://localhost:8501" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Happy pitch evaluating!" -ForegroundColor Magenta
Write-Host ""
