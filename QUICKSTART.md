# 🚀 Quick Start Guide

## Setup (One-time)

```powershell
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
copy .env.example .env

# 5. Edit .env and add your GROQ API key
# GROQ_API_KEY=your_key_here
```

## Run the App

```powershell
# Make sure venv is activated
.\.venv\Scripts\Activate.ps1

# Run Streamlit
streamlit run app.py
```

## Upload & Analyze

1. Open browser to `http://localhost:8501`
2. Upload a pitch video (MP4, MOV, etc.) - max 3 minutes
3. Wait 2-5 minutes for processing
4. Review results across 5 tabs:
   - 📝 Transcript
   - 🎤 Delivery Analysis (confidence, expressiveness, etc.)
   - 📊 Content Scores (6 dimensions + structure + viability)
   - 🦈 Shark Panel (4 AI investors + panel decision)
   - 📋 Summary (executive overview)

## Troubleshooting

**Missing GROQ_API_KEY:**
- Get a free key at https://console.groq.com
- Add it to your `.env` file

**FFmpeg not found:**
- Download from https://ffmpeg.org/download.html
- Add to system PATH

**Import errors:**
- Make sure venv is activated: `.\.venv\Scripts\Activate.ps1`
- Reinstall: `pip install -r requirements.txt --force-reinstall`

**Slow processing:**
- Normal for first run (downloads Whisper model)
- Subsequent runs are faster (~2-3 minutes)

## Architecture Overview

```
Video Upload
    ↓
Audio Extraction (trim to 3 min)
    ↓
[Parallel Processing]
    ├─→ Transcription (faster-whisper)
    └─→ Tone Analysis (librosa)
    ↓
Content Analysis (LLM: 6 dimensions + structure)
    ↓
Business Viability (LLM: aggregated assessment)
    ↓
Shark Panel (LangGraph: 4 AI investors)
    ↓
Results Display (Streamlit tabs)
```

## Key Features

✅ **Enhanced Tone Analysis**: Confidence, expressiveness, pitch, energy, silence ratio  
✅ **6 Business Dimensions**: Problem clarity, differentiation, business model, market, revenue, competition  
✅ **Pitch Structure**: Hook → Problem → Solution → Ask detection  
✅ **Business Viability**: Score, risk level, strengths, and weaknesses  
✅ **4 Shark Personas**: Visionary, Finance Shark, Customer Advocate, Skeptic  
✅ **Panel Consensus**: Aggregated decision (Invest / Not Invest / Need More Info)  

## Example Output

**Delivery Scores:**
- Confidence: 78/100
- Expressiveness: 65/100
- Overall Delivery: 71/100

**Top Dimension:**
- Problem Clarity: 92/100 ✨

**Panel Decision:**
- 🦈 **INVEST** (3 invest, 1 need more info)

Enjoy your pitch evaluation! 🎉
