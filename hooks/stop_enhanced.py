#!/usr/bin/env python3
"""
Enhanced Stop hook - announces Claude's task completion with summary.
Reads Claude's last response and creates informative speech notification.
"""
import json
import sys
import subprocess
import os
from pathlib import Path


def get_terminal_identifier():
    """Get human-readable terminal identifier."""
    # Check for custom environment variable
    custom_name = os.environ.get("CLAUDE_TERMINAL_NAME", None)
    if custom_name:
        return custom_name

    # Use TTY information
    try:
        tty = os.ttyname(sys.stdin.fileno()) if sys.stdin.isatty() else None
        if tty:
            terminal_num = tty.split('/')[-1]
            return f"Terminal {terminal_num}"
    except:
        pass

    return "Claude session"


def extract_summary(messages, max_words=30):
    """Extract key points from Claude's last message."""
    if not messages or len(messages) == 0:
        return "Task completed"

    # Get last assistant message
    last_msg = ""
    for msg in reversed(messages):
        if msg.get('role') == 'assistant':
            last_msg = msg.get('content', '')
            break

    if not last_msg:
        return "Task completed"

    # Look for completion indicators
    if "✅" in last_msg:
        # Find completed tasks
        lines = [l.strip() for l in last_msg.split('\n') if '✅' in l]
        if lines:
            # Take first completed item, remove emoji
            summary = lines[0].replace('✅', '').strip()
            words = summary.split()[:max_words]
            return ' '.join(words)

    # Look for errors
    if "❌" in last_msg or "Error:" in last_msg or "Failed:" in last_msg:
        lines = [l for l in last_msg.split('\n') if '❌' in l or 'Error' in l or 'Failed' in l]
        if lines:
            summary = lines[0].replace('❌', '').strip()
            words = summary.split()[:max_words]
            return ' '.join(words)

    # Look for "Summary:" or "## Summary" sections
    if "Summary:" in last_msg or "## Summary" in last_msg:
        lines = last_msg.split('\n')
        in_summary = False
        summary_lines = []
        for line in lines:
            if 'Summary:' in line or '## Summary' in line:
                in_summary = True
                continue
            if in_summary:
                if line.strip() and not line.startswith('#'):
                    summary_lines.append(line.strip())
                if len(summary_lines) >= 2 or len(' '.join(summary_lines).split()) >= max_words:
                    break
        if summary_lines:
            summary = ' '.join(summary_lines)
            words = summary.split()[:max_words]
            return ' '.join(words)

    # Default: first sentence
    sentences = last_msg.split('.')
    if sentences and sentences[0]:
        words = sentences[0].split()[:max_words]
        return ' '.join(words)

    return "Task completed"


def main():
    """Hook entry point."""
    try:
        # Read hook data
        raw_data = sys.stdin.read()
        data = json.loads(raw_data)

        # Load config
        import yaml
        config_path = Path.home() / ".claude" / "plugins" / "speech-automation" / "config.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)

        if not config.get("enabled", False):
            return

        # Get terminal identifier
        terminal = get_terminal_identifier()

        # Extract messages from session
        messages = data.get("messages", [])

        # Generate summary
        summary = extract_summary(messages, max_words=25)

        # Build message
        message = f"{terminal} finished. {summary}"

        # Speak
        script_path = Path(__file__).parent.parent / "scripts" / "speak.py"
        python_path = Path.home() / ".claude" / "plugins" / "speech-automation" / ".venv" / "bin" / "python"

        subprocess.Popen(
            [str(python_path), str(script_path), message, "af_bella", "1.0"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    except Exception as e:
        # Debug: log errors
        debug_log = Path.home() / ".claude" / "plugins" / "speech-automation" / "stop_debug.log"
        with open(debug_log, 'a') as f:
            f.write(f"Stop hook error: {e}\n")


if __name__ == "__main__":
    main()
