# Speech Automation Hooks Setup

## Overview

The speech-automation plugin includes **automatic speech hooks** that trigger notifications for:
- Long-running operations (30+ seconds)
- Errors and failures
- Test results
- Build completions
- Git operations

## Prerequisites

The hooks are **disabled by default**. To enable them:

1. The plugin must be installed
2. Hooks must be registered in Claude Code settings
3. Automation must be enabled via `/speech-config enable`

## Installation

### Step 1: Add Hooks to Settings

Add the following to your `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash|Task|WebFetch|WebSearch",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/plugins/cache/speech-automation-local/speech-automation/1.0.0/hooks/post_tool_use.py",
            "timeout": 5000
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/plugins/cache/speech-automation-local/speech-automation/1.0.0/hooks/session_start.py",
            "timeout": 2000
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/plugins/cache/speech-automation-local/speech-automation/1.0.0/hooks/stop.py",
            "timeout": 2000
          }
        ]
      }
    ]
  }
}
```

**Note:** Replace the version `1.0.0` with your installed version if different.

### Step 2: Enable Automation

Restart Claude Code, then run:
```
/speech-config enable
```

### Step 3: Verify Hooks are Active

Check that hooks are registered:
```
/hooks
```

You should see the speech-automation hooks listed.

## Usage

### Enable/Disable Automation

```bash
# Enable automatic speech
/speech-config enable

# Disable automatic speech
/speech-config disable

# View current settings
/speech-config
```

### Configure Event Types

```bash
# Disable error notifications
/speech-config set events.errors.enabled false

# Enable git operation notifications
/speech-config set events.git_operations.enabled true

# Adjust sensitivity (higher = fewer notifications)
/speech-config set min_priority 50
```

### Test Hooks

```bash
# Test long-running operation (should trigger after 35 seconds)
sleep 35 && echo "Done"

# Test error detection
python3 -c "raise ValueError('Test error')"
```

## How It Works

1. **PostToolUse Hook**: Monitors all tool executions (Bash, Task, etc.)
   - Checks if operation took 30+ seconds or had errors
   - Calculates priority score (0-100)
   - If priority ≥ min_priority, triggers speech

2. **SessionStart Hook**: Plays welcome message when automation is enabled

3. **Stop Hook**: Plays goodbye message when session ends (if automation enabled)

## Troubleshooting

### Hooks Not Running

1. Check hooks are registered: `/hooks`
2. Check automation is enabled: `/speech-config`
3. Check logs: `~/.claude/logs/` for hook errors
4. Verify hook scripts are executable: `chmod +x ~/.claude/plugins/cache/speech-automation-local/speech-automation/1.0.0/hooks/*.py`

### No Speech Triggered

1. Check `enabled: true` in config: `/speech-config`
2. Lower priority threshold: `/speech-config set min_priority 10`
3. Check event type is enabled: `/speech-config`
4. Wait for rate limit to expire (default: 60 seconds between same event type)

### Hooks Timing Out

If hooks timeout (default 5 seconds for PostToolUse):
```json
{
  "hooks": {
    "PostToolUse": [{
      "hooks": [{
        "timeout": 10000  // Increase to 10 seconds
      }]
    }]
  }
}
```

## Advanced Configuration

### Quiet Hours

Hooks respect quiet hours configuration (10 PM - 7 AM by default):

```bash
# Change quiet hours
/speech-config set quiet_hours.start_hour 23
/speech-config set quiet_hours.end_hour 6

# Disable quiet hours
/speech-config set quiet_hours.enabled false
```

### Event-Specific Voices

```bash
# Use different voice for errors
/speech-config set events.errors.voice bf_emma

# Use different voice for tests
/speech-config set events.test_results.voice am_michael
```

### Rate Limiting

```bash
# Allow notifications more frequently
/speech-config set rate_limit_seconds 30

# Less frequent notifications
/speech-config set rate_limit_seconds 120
```

## Uninstalling Hooks

To remove hooks:

1. Edit `.claude/settings.json` and remove the hooks entries
2. Or use `/hooks` menu and delete the speech-automation hooks

## Security Note

Hooks run with your user permissions. The speech-automation hooks only:
- Read config.yaml
- Call the speech-tts MCP server
- Write logs to stderr

No file modifications or external network calls (except to ML server via MCP).
