# 🦈 Pitch Evaluation Studio

A production-grade AI-powered pitch evaluation system with a virtual Shark Tank panel. Upload your startup pitch video and get comprehensive feedback on your delivery, content, and business viability.

DEMO : https://pitch-evaluation-studio.streamlit.app/
## 🌟 Features

- **🎤 Vocal Delivery Analysis**: Confidence, expressiveness, pitch variation, energy levels
- **📊 Content Evaluation**: 6-dimension business analysis (problem clarity, differentiation, business model, market, revenue, competition)
- **🏗️ Pitch Structure Detection**: Hook → Problem → Solution → Ask analysis
- **💼 Business Viability Scoring**: Risk assessment with strengths and weaknesses
- **🦈 Virtual Shark Tank Panel**: 4 AI investor personas providing personalized feedback:
  - 🔮 The Visionary (market potential & innovation)
  - 💰 The Finance Shark (revenue & profitability)
  - ❤️ The Customer Advocate (problem-solution fit)
  - 🤔 The Skeptic (risks & competition)

## 📁 Project Structure

```
PitchEvaluation/
├── app.py              # Streamlit UI with tabs and real-time updates
├── pipeline.py         # Orchestrates the full evaluation pipeline
├── audio.py            # Video → audio extraction (trims to 3 min)
├── transcribe.py       # Speech-to-text using faster-whisper
├── tone.py             # Vocal delivery analysis using librosa
├── main.py             # LLM-based content analysis chains
├── agents.py           # LangGraph shark panel (4 sharks + aggregator)
├── prompts.py          # Centralized prompt templates with few-shot examples
├── parsers.py          # Pydantic output schemas
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- FFmpeg (for video/audio processing)
- GROQ API key ([get one here](https://console.groq.com))

### Installation

1. **Clone and navigate to the project:**
```powershell
cd PitchEvaluation
```

2. **Create virtual environment and install dependencies:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. **Set up environment variables:**
```powershell
copy .env.example .env
# Edit .env and add your GROQ_API_KEY
```

4. **Run the Streamlit app:**
```powershell
streamlit run app.py
```

5. **Open your browser** to `http://localhost:8501`

## 🎯 Usage

1. Upload your pitch video (MP4, MOV, MKV, or AVI - max 3 minutes)
2. Wait for the pipeline to process (2-5 minutes depending on video length)
3. Review results across 5 tabs:
   - **Transcript**: What you said
   - **Delivery Analysis**: Voice confidence, expressiveness, pacing
   - **Content Scores**: 6 business dimensions + structure + viability
   - **Shark Panel**: Individual feedback from 4 AI investors + panel decision
   - **Summary**: Executive overview with key takeaways

## 🔧 How It Works

1. **Audio Extraction** (parallel): Extracts and trims audio to 3 minutes
2. **Parallel Processing**:
   - Transcription using `faster-whisper` (small model, CPU-optimized)
   - Tone analysis using `librosa` (pitch, energy, silence detection)
3. **Content Analysis**: LLM evaluates 6 dimensions + pitch structure in parallel
4. **Viability Assessment**: Second-stage LLM aggregates dimension scores
5. **Shark Panel**: 4 AI personas evaluate independently, then panel aggregates

## 🧠 Technology Stack

- **UI**: Streamlit with custom CSS
- **LLM**: Groq (Llama 3.3 70B) via langchain-groq
- **Audio**: librosa, moviepy, soundfile
- **Transcription**: faster-whisper (OpenAI Whisper optimized)
- **Agents**: LangGraph for multi-agent orchestration
- **Validation**: Pydantic v2

## 📊 Evaluation Dimensions

1. **Problem Clarity**: How well you articulate the customer pain
2. **Product Differentiation**: Unique value vs. competitors
3. **Business Model Strength**: Monetization clarity
4. **Market Opportunity**: TAM/SAM and growth potential
5. **Revenue Logic**: Pricing alignment with customer segment
6. **Competition Awareness**: Understanding of alternatives

## 🦈 Shark Personas

Each shark has a unique focus and evaluation style:
- **The Visionary**: Focuses on big picture, market size, long-term potential
- **The Finance Shark**: Numbers-driven, wants clear path to profitability
- **The Customer Advocate**: Empathizes with users, validates problem-solution fit
- **The Skeptic**: Challenges assumptions, identifies risks and weak spots

## 🛠️ Development

### Run individual modules:

**Test audio extraction:**
```python
from audio import extract_audio_from_video
extract_audio_from_video("video.mp4", "output.wav", max_duration_sec=180)
```

**Test transcription:**
```python
from transcribe import transcribe_audio
transcript, segments = transcribe_audio("audio.wav")
```

**Test tone analysis:**
```python
from tone import analyze_tone
tone_scores = analyze_tone("audio.wav")
```

**Test content analysis:**
```python
from main import analyze_pitch_with_viability
analysis = analyze_pitch_with_viability("transcript text here...")
```

**Test shark panel:**
```python
from agents import run_shark_panel
result = run_shark_panel(transcript, tone_scores, analysis)
```

## 📝 Notes

- Videos longer than 3 minutes are automatically trimmed to the first 3 minutes
- The system uses CPU-optimized models (no GPU required)
- Average processing time: 2-5 minutes per video
- All LLM calls use Groq's fast inference (Llama 3.3 70B)
- The shark panel uses LangGraph for parallel agent execution

## 🔒 Environment Variables

Create a `.env` file with:
```env
GROQ_API_KEY=your_groq_api_key_here
```

## 📄 License

This project is for educational and evaluation purposes.

## 🙏 Acknowledgments

Based on the original Colab notebook, refactored into a production-grade modular architecture.
