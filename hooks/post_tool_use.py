#!/usr/bin/env python3
"""
PostToolUse hook for automatic speech notifications.
Triggers TTS for important events via direct subprocess call.
"""
import json
import sys
import subprocess
from pathlib import Path


def load_config() -> dict:
    """Load YAML config with sensible defaults."""
    try:
        import yaml
        # Config is in the plugin source directory, not cache
        config_path = Path.home() / ".claude" / "plugins" / "speech-automation" / "config.yaml"
        with open(config_path) as f:
            return yaml.safe_load(f)
    except Exception:
        return {"enabled": False}


def classify_event(tool_name: str, result: str, duration_ms: int) -> tuple:
    """
    Classify event type and generate message.

    Returns: (event_type, message, voice, should_speak)
    """
    config = load_config()

    # Check global enable
    if not config.get("enabled", False):
        return (None, None, None, False)

    # Long-running operations (30+ seconds)
    if duration_ms >= 30000:
        event_config = config.get("events", {}).get("long_running", {})
        if event_config.get("enabled", False):
            seconds = duration_ms // 1000
            voice = event_config.get("voice", "af_bella")
            return (
                "long_running",
                f"Long operation completed after {seconds} seconds",
                voice,
                True
            )

    # Errors and exceptions
    if "error" in result.lower() or "exception" in result.lower() or "traceback" in result.lower():
        event_config = config.get("events", {}).get("errors", {})
        if event_config.get("enabled", False):
            voice = event_config.get("voice", "af_bella")
            return (
                "error",
                f"Error detected in {tool_name} operation",
                voice,
                True
            )

    # Git operations
    if tool_name == "Bash":
        # Extract command from arguments
        command = result.lower() if result else ""
        if "git" in command or "commit" in command or "push" in command or "pull" in command:
            event_config = config.get("events", {}).get("git_operations", {})
            if event_config.get("enabled", False):
                voice = event_config.get("voice", "af_bella")
                return (
                    "git",
                    "Git operation completed",
                    voice,
                    True
                )

    # Test results
    if "test" in result.lower() or "pytest" in result.lower() or "jest" in result.lower():
        event_config = config.get("events", {}).get("test_results", {})
        if event_config.get("enabled", False):
            voice = event_config.get("voice", "af_bella")

            # Check pass/fail preference
            if "passed" in result.lower() or "ok" in result.lower():
                if event_config.get("speak_on_pass", False):
                    return ("test_pass", "Tests passed", voice, True)
            elif "failed" in result.lower() or "error" in result.lower():
                if event_config.get("speak_on_fail", True):
                    return ("test_fail", "Tests failed", voice, True)

    # Build completion
    if "build" in result.lower() or "webpack" in result.lower() or "vite" in result.lower():
        event_config = config.get("events", {}).get("build_completion", {})
        if event_config.get("enabled", False):
            voice = event_config.get("voice", "af_bella")
            return (
                "build",
                "Build completed",
                voice,
                True
            )

    return (None, None, None, False)


def trigger_speech(message: str, voice: str = "af_bella", speed: float = 1.0) -> None:
    """Trigger TTS via subprocess (non-blocking)."""
    try:
        script_path = Path(__file__).parent.parent / "scripts" / "speak.py"
        # venv is in the plugin source directory, not cache
        python_path = Path.home() / ".claude" / "plugins" / "speech-automation" / ".venv" / "bin" / "python"

        # Launch TTS in background
        subprocess.Popen(
            [str(python_path), str(script_path), message, voice, str(speed)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        # Silent failure - hooks must never crash
        pass


def main():
    """Hook entry point."""
    try:
        # Read hook data from stdin
        data = json.loads(sys.stdin.read())

        tool_name = data.get("tool", {}).get("name", "")
        result = str(data.get("result", ""))
        duration_ms = data.get("duration_ms", 0)

        # Classify and trigger
        event_type, message, voice, should_speak = classify_event(tool_name, result, duration_ms)

        if should_speak and message:
            trigger_speech(message, voice)

    except Exception:
        # Hooks must never crash Claude Code
        pass


if __name__ == "__main__":
    main()
