from faster_whisper import WhisperModel
from typing import Tuple, List


def transcribe_audio(audio_path: str, model_size: str = "small", device: str = "cpu") -> Tuple[str, List[dict]]:
    """Transcribe the audio using faster-whisper and return (transcript, segments).

    Segments is a list of dicts with keys like 'start', 'end', 'text'.
    """
    model = WhisperModel(model_size, device=device, compute_type="int8")
    segments, info = model.transcribe(audio_path, beam_size=1, best_of=1, vad_filter=True)

    texts = []
    segments_list = []
    for seg in segments:
        segments_list.append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text,
        })
        texts.append(seg.text)

    transcript = "".join(texts).strip()
    return transcript, segments_list


__all__ = ["transcribe_audio"]
