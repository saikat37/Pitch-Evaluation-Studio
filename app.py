"""Streamlit front-end for Pitch Evaluation.

Features:
- Upload a video (max 3 minutes). Audio extraction trims to 3 minutes.
- Shows live progress updates for each pipeline stage.
- Displays transcript, enhanced tone metrics, content analysis, and full shark panel feedback.

Run: `streamlit run app.py`
"""
import streamlit as st
import tempfile
import os
from pathlib import Path
from dotenv import load_dotenv
from logging_config import setup_logging
from pipeline import run_pipeline

load_dotenv()

# Initialize logging once
if 'logging_initialized' not in st.session_state:
    setup_logging("logs/pitch_evaluation.log")
    st.session_state.logging_initialized = True


st.set_page_config(page_title="🦈 Pitch Evaluation Studio", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .shark-feedback {
        background-color: #e3f2fd;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1E88E5;
        margin: 1rem 0;
    }
    .decision-invest {
        color: #4CAF50;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .decision-not-invest {
        color: #F44336;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .decision-need-info {
        color: #FF9800;
        font-weight: bold;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🦈 Pitch Evaluation Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload your pitch video and get AI-powered feedback from our virtual Shark Tank panel</div>', unsafe_allow_html=True)

uploaded = st.file_uploader("📹 Upload your pitch video (MP4, MOV, MKV, AVI - max 3 minutes)", 
                            type=["mp4", "mov", "mkv", "avi"], 
                            accept_multiple_files=False)

# Progress tracking
if 'progress_messages' not in st.session_state:
    st.session_state.progress_messages = []

progress_placeholder = st.empty()
status_placeholder = st.empty()

def ui_callback(stage, payload):
    """Called from pipeline to update the UI with beautiful progress."""
    # Create user-friendly messages
    stage_icons = {
        "start": "🚀",
        "extract_audio": "🎵",
        "extract_audio.done": "✅",
        "parallel.start": "⚡",
        "transcribe.done": "📝",
        "tone.done": "🎤",
        "parallel.done": "✅",
        "content.start": "🧠",
        "content.done": "✅",
        "sharks.start": "🦈",
        "sharks.done": "🎯",
        "complete": "🎉"
    }
    
    stage_names = {
        "start": "Initializing Pipeline",
        "extract_audio": "Extracting Audio",
        "extract_audio.done": "Audio Ready",
        "parallel.start": "Analyzing in Parallel",
        "transcribe.done": "Transcription Complete",
        "tone.done": "Tone Analysis Complete",
        "parallel.done": "Parallel Analysis Complete",
        "content.start": "Evaluating Content",
        "content.done": "Content Analysis Complete",
        "sharks.start": "Consulting Shark Panel",
        "sharks.done": "Shark Feedback Ready",
        "complete": "All Done!"
    }
    
    icon = stage_icons.get(stage, "⚙️")
    name = stage_names.get(stage, stage)
    
    # Add to session state
    st.session_state.progress_messages.append(f"{icon} {name}")
    
    # Update UI
    with status_placeholder.container():
        st.info(f"**Current:** {icon} {name}")
    
    with progress_placeholder.container():
        st.markdown("### 📊 Progress Timeline")
        for i, msg in enumerate(st.session_state.progress_messages[-8:], 1):
            st.markdown(f"{i}. {msg}")
        st.markdown("---")


if uploaded:
    # Use file name as unique identifier to prevent duplicate processing
    file_id = f"{uploaded.name}_{uploaded.size}"
    
    # Check if we've already processed this file
    if 'last_processed_file' not in st.session_state or st.session_state.last_processed_file != file_id:
        # Reset progress messages
        st.session_state.progress_messages = []
        
        # Save to a temp file
        t = tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded.name).suffix)
        t.write(uploaded.read())
        t.flush()
        t.close()

        st.info("🎬 File uploaded successfully! Starting analysis pipeline...")
        
        with st.spinner("🔄 Processing your pitch..."):
            results = run_pipeline(t.name, callback=ui_callback)
        
        # Store results in session state
        st.session_state.results = results
        st.session_state.last_processed_file = file_id
        
        # Clean up temp file
        try:
            os.remove(t.name)
        except:
            pass
    else:
        # Use cached results
        results = st.session_state.results

    st.success("✅ Analysis complete! Here are your results:")
    
    # Create tabs for organized display
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Transcript", "🎤 Delivery Analysis", "📊 Content Scores", "🦈 Shark Panel", "📋 Summary"])
    
    with tab1:
        st.header("📝 Transcript")
        transcript = results.get("transcript", "")
        st.text_area("What you said:", value=transcript, height=300, disabled=True)
        st.caption(f"Word count: ~{len(transcript.split())} words")
    
    with tab2:
        st.header("🎤 Vocal Delivery Analysis")
        tone = results.get("tone_scores", {})
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🎯 Confidence", f"{tone.get('confidence_score', 0):.0f}/100")
        col2.metric("✨ Expressiveness", f"{tone.get('expressiveness_score', 0):.0f}/100")
        col3.metric("🎭 Overall Delivery", f"{tone.get('delivery_score', 0):.0f}/100")
        col4.metric("⚡ Speaking Rate", f"{tone.get('speaking_rate', 0):.0f} BPM")
        
        st.subheader("Detailed Metrics")
        col5, col6, col7, col8 = st.columns(4)
        col5.metric("🎵 Avg Pitch", f"{tone.get('pitch_mean', 0):.0f} Hz")
        col6.metric("📈 Pitch Variation", f"{tone.get('pitch_std', 0):.1f}")
        col7.metric("🔊 Energy Level", f"{tone.get('energy_mean', 0):.3f}")
        col8.metric("🤫 Silence Ratio", f"{tone.get('silence_ratio', 0):.1%}")
    
    with tab3:
        st.header("📊 Business Content Analysis")
        analysis = results.get("analysis", {})
        dimensions = analysis.get("dimensions", {})
        
        # Dimension scores in a clean layout
        st.subheader("Core Dimensions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💡 Problem Clarity", f"{dimensions.get('problem_clarity', {}).get('score', 0)}/100")
            st.caption(dimensions.get('problem_clarity', {}).get('reason', 'N/A'))
            
            st.metric("🎯 Product Differentiation", f"{dimensions.get('product_differentiation', {}).get('score', 0)}/100")
            st.caption(dimensions.get('product_differentiation', {}).get('reason', 'N/A'))
        
        with col2:
            st.metric("💰 Business Model", f"{dimensions.get('business_model_strength', {}).get('score', 0)}/100")
            st.caption(dimensions.get('business_model_strength', {}).get('reason', 'N/A'))
            
            st.metric("📈 Market Opportunity", f"{dimensions.get('market_opportunity', {}).get('score', 0)}/100")
            st.caption(dimensions.get('market_opportunity', {}).get('reason', 'N/A'))
        
        with col3:
            st.metric("💵 Revenue Logic", f"{dimensions.get('revenue_logic', {}).get('score', 0)}/100")
            st.caption(dimensions.get('revenue_logic', {}).get('reason', 'N/A'))
            
            st.metric("🏢 Competition Awareness", f"{dimensions.get('competition_awareness', {}).get('score', 0)}/100")
            st.caption(dimensions.get('competition_awareness', {}).get('reason', 'N/A'))
        
        # Pitch structure
        st.subheader("🎯 Pitch Structure")
        structure = analysis.get("pitch_structure", {})
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric("Structure Quality", f"{structure.get('structure_quality_score', 0)}/100")
            st.write("**Elements Present:**")
            st.write(f"- Hook: {'✅' if structure.get('hook_present') else '❌'}")
            st.write(f"- Problem: {'✅' if structure.get('problem_present') else '❌'}")
            st.write(f"- Solution: {'✅' if structure.get('solution_present') else '❌'}")
            st.write(f"- Ask: {'✅' if structure.get('ask_present') else '❌'}")
        with col_s2:
            st.write("**Detected Order:**")
            st.write(" → ".join(structure.get('detected_order', [])))
            st.caption(structure.get('structure_comment', ''))
        
        # Business viability
        st.subheader("🎯 Business Viability")
        viability = analysis.get("business_viability", {})
        col_v1, col_v2, col_v3 = st.columns(3)
        col_v1.metric("Viability Score", f"{viability.get('score', 0)}/100")
        col_v2.metric("Risk Level", viability.get('risk_level', 'N/A').upper())
        
        st.write("**Summary:**", viability.get('summary_comment', 'N/A'))
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            st.write("**💪 Key Strengths:**")
            for strength in viability.get('key_strengths', []):
                if strength:
                    st.write(f"- {strength}")
        with col_k2:
            st.write("**⚠️ Key Risks:**")
            for risk in viability.get('key_risks', []):
                if risk:
                    st.write(f"- {risk}")
    
    with tab4:
        st.header("🦈 Shark Tank Panel Evaluation")
        shark_panel = results.get("shark_panel", {})
        
        # Panel decision at the top
        st.subheader("🎯 Final Panel Decision")
        decision = shark_panel.get("panel_final_recommendation", "N/A")
        decision_class = "decision-invest" if decision == "Invest" else ("decision-not-invest" if decision == "Not Invest" else "decision-need-info")
        st.markdown(f'<div class="{decision_class}">📢 {decision}</div>', unsafe_allow_html=True)
        
        st.markdown("**Panel Consensus:**")
        panel_feedback = shark_panel.get("panel_combined_feedback", "N/A")
        st.info(panel_feedback)
        
        # Text-to-Speech for Panel Consensus (Streamlit Cloud compatible - in-memory)
        if panel_feedback and panel_feedback != "N/A":
            try:
                from gtts import gTTS
                from io import BytesIO
                
                # Generate unique audio for this session
                audio_key = f"panel_audio_{hash(panel_feedback)}"
                if audio_key not in st.session_state:
                    # Generate TTS audio in-memory (no file system writes)
                    tts = gTTS(text=panel_feedback, lang='en', slow=False)
                    audio_buffer = BytesIO()
                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)
                    st.session_state[audio_key] = audio_buffer.read()
                
                # Auto-play the audio from memory
                st.audio(st.session_state[audio_key], format='audio/mp3', autoplay=True)
                st.caption("🔊 Playing panel consensus...")
                
            except Exception as e:
                st.caption(f"⚠️ TTS unavailable: {str(e)}")
        
        st.divider()
        
        # Individual shark feedback
        st.subheader("Individual Shark Opinions")
        
        sharks = [
            ("🔮 The Visionary", "visionary", "#E3F2FD"),
            ("💰 The Finance Shark", "finance_shark", "#FFF3E0"),
            ("❤️ The Customer Advocate", "customer_advocate", "#F3E5F5"),
            ("🤔 The Skeptic", "skeptic", "#FFEBEE"),
        ]
        
        for name, key, color in sharks:
            with st.expander(f"{name}", expanded=True):
                feedback = shark_panel.get(f"{key}_feedback", "N/A")
                decision = shark_panel.get(f"{key}_decision", "N/A")
                
                st.markdown(f'<div style="background-color: {color}; padding: 1rem; border-radius: 0.5rem;">', unsafe_allow_html=True)
                st.write(feedback)
                decision_class = "decision-invest" if decision == "Invest" else ("decision-not-invest" if decision == "Not Invest" else "decision-need-info")
                st.markdown(f'<div class="{decision_class}">Decision: {decision}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        st.header("📋 Executive Summary")
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Overall Delivery", f"{tone.get('delivery_score', 0):.0f}/100")
        col2.metric("Confidence", f"{tone.get('confidence_score', 0):.0f}/100")
        viability = analysis.get("business_viability", {})
        col3.metric("Business Viability", f"{viability.get('score', 0)}/100")
        col4.metric("Panel Decision", shark_panel.get("panel_final_recommendation", "N/A"))
        
        st.subheader("Key Takeaways")
        st.write("**Top 3 Dimensions:**")
        dim_scores = [(k, v.get('score', 0)) for k, v in dimensions.items()]
        dim_scores.sort(key=lambda x: x[1], reverse=True)
        for i, (dim, score) in enumerate(dim_scores[:3], 1):
            st.write(f"{i}. {dim.replace('_', ' ').title()}: {score}/100")
        
        st.write("**Areas for Improvement:**")
        for i, (dim, score) in enumerate(dim_scores[-3:], 1):
            st.write(f"{i}. {dim.replace('_', ' ').title()}: {score}/100")

    # Cleanup uploaded temp file
    try:
        os.remove(t.name)
    except Exception:
        pass

else:
    # Landing page
    st.markdown("### 🚀 How it works:")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("#### 1️⃣ Upload")
        st.write("Upload your pitch video (max 3 minutes)")
    with col2:
        st.markdown("#### 2️⃣ Analyze")
        st.write("AI analyzes your delivery, content & business model")
    with col3:
        st.markdown("#### 3️⃣ Evaluate")
        st.write("4 virtual sharks provide personalized feedback")
    with col4:
        st.markdown("#### 4️⃣ Improve")
        st.write("Get actionable insights to refine your pitch")
    
    st.markdown("---")
    st.info("💡 **Tip**: Practice your pitch, record it, and upload here to get instant feedback from our AI shark panel!")
