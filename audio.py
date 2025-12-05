import os
import tempfile
from moviepy.editor import VideoFileClip


def extract_audio_from_video(video_path: str, out_wav: str, max_duration_sec: int = None):
    """Extract audio from `video_path` and save as 16k PCM WAV to `out_wav`.

    - Trims to `max_duration_sec` seconds if specified and the video is longer.
    - Ensures sample rate 16k using moviepy's write_audiofile parameters.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(video_path)

    with VideoFileClip(video_path) as clip:
        duration = clip.duration
        if max_duration_sec and duration > max_duration_sec:
            clip = clip.subclip(0, max_duration_sec)

        # moviepy handles conversion; ensure ffmpeg is available on PATH
        clip.audio.write_audiofile(
            out_wav,
            fps=16000,
            nbytes=2,
            codec="pcm_s16le",
            verbose=False,
            logger=None,
        )

    return out_wav


def make_temp_wav_path(prefix: str = "pitch_") -> str:
    fd, path = tempfile.mkstemp(prefix=prefix, suffix=".wav")
    os.close(fd)
    return path


__all__ = ["extract_audio_from_video", "make_temp_wav_path"]
