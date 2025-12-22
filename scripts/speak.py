#!/usr/bin/env python3
"""
Minimal TTS CLI for hook integration.
Calls ML server directly, plays audio, fails silently.

Usage:
    speak.py "Hello world" [voice] [speed]
    speak.py "Error detected" af_bella 1.0
"""
import sys
import subprocess
from pathlib import Path


def speak(text: str, voice: str = "af_bella", speed: float = 1.0) -> None:
    """Synthesize speech and play audio."""
    try:
        # Import here to avoid startup overhead
        import httpx
        import base64

        # Call ML server TTS endpoint
        response = httpx.post(
            "http://ml-server:8001/tts/synthesize",
            json={
                "text": text,
                "voice": voice,
                "speed": speed,
                "format": "wav"
            },
            timeout=30.0
        )
        response.raise_for_status()

        # Decode base64 audio
        audio_bytes = base64.b64decode(response.json()["audio_data"])

        # Save to cache directory
        cache_dir = Path.home() / ".cache" / "speech-mcp"
        cache_dir.mkdir(parents=True, exist_ok=True)

        audio_file = cache_dir / f"hook_{abs(hash(text))}.wav"
        audio_file.write_bytes(audio_bytes)

        # Play audio in background (macOS)
        subprocess.Popen(
            ["afplay", str(audio_file)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    except Exception:
        # Fail silently - hooks must never crash Claude Code
        pass


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "Hello"
    voice = sys.argv[2] if len(sys.argv) > 2 else "af_bella"
    speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0

    speak(text, voice, speed)
