"""Pipeline orchestrator.
Runs audio extraction, transcription and tone analysis in parallel, then runs
content analysis, and finally runs the shark panel evaluation.
Provides callback hooks so the UI can receive updates.
"""
import concurrent.futures
import os
from typing import Callable, Dict
from logging_config import get_logger

from audio import extract_audio_from_video, make_temp_wav_path
from transcribe import transcribe_audio
from tone import analyze_tone
from main import analyze_pitch_with_viability
from agents import run_shark_panel

logger = get_logger(__name__)


def run_pipeline(video_path: str, callback: Callable[[str, Dict], None] = None) -> Dict:
    """Run the full pipeline and call `callback(stage, payload)` as stages progress.

    Stages: extract_audio, transcribe, tone, analysis, shark_panel, done
    """
    logger.info("=" * 60)
    logger.info("Starting pipeline for video: %s", video_path)
    
    temp_wav = make_temp_wav_path()
    if callback:
        callback("start", {})

    # 1) extract audio
    logger.info("Stage 1: Extracting audio (entire video)")
    if callback:
        callback("extract_audio", {})
    extract_audio_from_video(video_path, temp_wav, max_duration_sec=None)
    logger.info("Audio extracted to: %s", temp_wav)
    if callback:
        callback("extract_audio.done", {})

    # 2) run transcription and tone analysis in parallel
    logger.info("Stage 2: Running transcription and tone analysis in parallel")
    if callback:
        callback("parallel.start", {})

    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        fut_trans = ex.submit(transcribe_audio, temp_wav)
        fut_tone = ex.submit(analyze_tone, temp_wav)

        for fut in concurrent.futures.as_completed([fut_trans, fut_tone]):
            if fut is fut_trans:
                transcript, segments = fut.result()
                results["transcript"] = transcript
                results["segments"] = segments
                logger.info("Transcription complete: %d words", len(transcript.split()))
                if callback:
                    callback("transcribe.done", {})
            else:
                tone_scores = fut.result()
                results["tone_scores"] = tone_scores
                logger.info("Tone analysis complete: confidence=%.1f, delivery=%.1f", 
                          tone_scores.get('confidence_score', 0),
                          tone_scores.get('delivery_score', 0))
                if callback:
                    callback("tone.done", {})
    
    if callback:
        callback("parallel.done", {})

    # 3) run content analysis / viability
    logger.info("Stage 3: Analyzing content and business viability")
    if callback:
        callback("content.start", {})
    analysis = analyze_pitch_with_viability(results.get("transcript", ""))
    results["analysis"] = analysis
    logger.info("Content analysis complete: viability_score=%d", 
               analysis.get('viability', {}).get('score', 0))
    if callback:
        callback("content.done", {})
    
    # Small delay between stages to avoid rate limits
    import time
    time.sleep(1)

    # 4) run shark panel evaluation (runs sequentially: visionary → finance → customer → skeptic → panel)
    logger.info("Stage 4: Running shark panel evaluation")
    if callback:
        callback("sharks.start", {})
    shark_result = run_shark_panel(
        transcript=results["transcript"],
        tone_scores=results["tone_scores"],
        analysis=analysis,
    )
    results["shark_panel"] = shark_result
    logger.info("Shark panel complete: final_recommendation=%s", 
               shark_result.get('panel', {}).get('final_recommendation', 'N/A'))
    if callback:
        callback("sharks.done", {})

    logger.info("Pipeline finished successfully")
    logger.info("=" * 60)
    if callback:
        callback("complete", {})

    # clean up temp wav
    try:
        os.remove(temp_wav)
    except Exception:
        pass

    return results


__all__ = ["run_pipeline"]
