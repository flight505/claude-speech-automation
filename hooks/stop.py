#!/usr/bin/env python3
"""
Stop hook - goodbye message.
Plays brief goodbye when Claude Code exits.
"""
import subprocess
from pathlib import Path


def main():
    """Hook entry point."""
    try:
        # Load config
        import yaml
        config_path = Path(__file__).parent.parent.parent / "config.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)

        # Only speak if automation enabled
        if not config.get("enabled", False):
            return

        # Trigger goodbye speech
        script_path = Path(__file__).parent.parent / "scripts" / "speak.py"
        python_path = Path(__file__).parent.parent.parent / ".venv" / "bin" / "python"

        subprocess.Popen(
            [str(python_path), str(script_path), "Session ended", "af_bella", "1.0"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    except Exception:
        # Silent failure - hooks must never crash
        pass


if __name__ == "__main__":
    main()
