#!/usr/bin/env python3
"""
SessionStart hook - welcome message.
Plays brief welcome when Claude Code starts.
"""
import subprocess
from pathlib import Path


def main():
    """Hook entry point."""
    try:
        # Load config from plugin source directory, not cache
        import yaml
        config_path = Path.home() / ".claude" / "plugins" / "speech-automation" / "config.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)

        # Only speak if automation enabled
        if not config.get("enabled", False):
            return

        # Trigger welcome speech
        script_path = Path(__file__).parent.parent / "scripts" / "speak.py"
        # venv is in the plugin source directory, not cache
        python_path = Path.home() / ".claude" / "plugins" / "speech-automation" / ".venv" / "bin" / "python"

        subprocess.Popen(
            [str(python_path), str(script_path), "Speech automation enabled", "af_bella", "1.0"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    except Exception:
        # Silent failure - hooks must never crash
        pass


if __name__ == "__main__":
    main()
