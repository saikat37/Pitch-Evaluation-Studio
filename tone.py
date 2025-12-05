import librosa
import numpy as np
from typing import Dict


def analyze_tone(audio_path: str) -> Dict:
    """Compute enhanced vocal delivery metrics from audio.

    Returns a dict with:
      - pitch_mean, pitch_std: pitch contour statistics
      - energy_mean, energy_std: loudness/volume statistics
      - speaking_rate: approximate tempo
      - silence_ratio: proportion of silence in audio
      - confidence_score: 0-100 based on energy and silence
      - expressiveness_score: 0-100 based on pitch and energy variation
      - delivery_score: 0-100 overall delivery quality
    """
    # 1. Load audio
    y, sr = librosa.load(audio_path, sr=16000)

    # ========= TONE & VOCAL DELIVERY FEATURES =========
    # A) Pitch contour → how high/low & how much it varies
    f0 = librosa.yin(y, fmin=50, fmax=300, sr=sr)
    pitch_mean = float(np.nanmean(f0))
    pitch_std = float(np.nanstd(f0))  # variation → monotone vs expressive

    # B) Energy (volume) → how loud & dynamic the voice is
    rms = librosa.feature.rms(y=y)[0]
    energy_mean = float(np.mean(rms))
    energy_std = float(np.std(rms))  # variation → flat vs energetic

    # C) Speaking rate / pace (approx)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    speaking_rate = float(tempo)

    # D) Pauses / silence ratio (very rough)
    intervals = librosa.effects.split(y, top_db=30)  # non-silent segments
    total_speech = sum((end - start) for start, end in intervals) / sr
    total_duration = len(y) / sr
    silence_ratio = float(1 - total_speech / total_duration)

    # ========= SIMPLE RULE-BASED SCORING (0–100) =========
    # Confidence score (energy + low silence)
    confidence = 0
    confidence += min(50, (energy_mean * 500))  # louder → more confident
    confidence += max(0, 50 * (1 - silence_ratio))  # less silence → more confident
    confidence = float(max(0, min(100, confidence)))

    # Expressiveness score (pitch & energy variation)
    expressiveness = 0
    expressiveness += min(60, pitch_std * 2)  # more pitch variation
    expressiveness += min(40, energy_std * 200)
    expressiveness = float(max(0, min(100, expressiveness)))

    # Overall delivery score = combination
    delivery_score = float((confidence * 0.5) + (expressiveness * 0.5))

    return {
        "pitch_mean": pitch_mean,
        "pitch_std": pitch_std,
        "energy_mean": energy_mean,
        "energy_std": energy_std,
        "speaking_rate": speaking_rate,
        "silence_ratio": silence_ratio,
        "confidence_score": confidence,
        "expressiveness_score": expressiveness,
        "delivery_score": delivery_score,
    }


__all__ = ["analyze_tone"]
