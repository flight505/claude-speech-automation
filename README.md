# Speech Automation Plugin

Intelligent speech notifications for Claude Code using Kokoro TTS.

## Features

- **🔊 Manual Speech Commands** - `/speak`, `/voices`, `/speech-status`, `/speech-config`
- **🤖 Automatic Speech Hooks** - Smart notifications for errors, tests, builds, and long operations
- **⚡ GPU-Accelerated** - Fast synthesis with Kokoro TTS 82M model
- **💾 Smart Caching** - 10,000x speedup for repeated phrases
- **🎭 8 Voices** - American and British, male and female
- **🎯 Priority Scoring** - Intelligent event classification (0-100 scale)
- **⏰ Quiet Hours** - Reduce or disable notifications at night (10 PM - 7 AM)

## Prerequisites

This plugin requires the **speech-tts MCP server** to be configured.

1. The speech-tts MCP server must be installed and configured via:
   ```bash
   claude mcp add speech-tts /path/to/Speech_MCP/start-mcp-server.sh
   ```

2. ML server must be running at http://ml-server:8001 with Kokoro TTS

## Installation

Install the plugin:
```bash
claude plugin install ~/.claude/plugins/speech-automation
```

Or for local development, the plugin can be loaded from:
```
~/.claude/plugins/speech-automation/
```

## Commands

### /speak
Synthesize speech from text:
```
/speak "Hello world"
/speak "Build complete" --voice am_adam --speed 1.2
```

### /voices
List all available voices:
```
/voices
/voices --play-samples
```

### /speech-status
Check system status:
```
/speech-status
```

### /speech-config
Configure automatic speech settings:
```
# View current configuration
/speech-config

# Enable/disable automation
/speech-config enable
/speech-config disable

# Adjust settings
/speech-config set min_priority 50
/speech-config set events.errors.enabled false
/speech-config set quiet_hours.start_hour 23
```

## Automatic Speech

**⚠️ Hooks are now installed! See [HOOKS-SETUP.md](HOOKS-SETUP.md) for details.**

The plugin includes intelligent hooks that automatically trigger speech for important events:

**Event Types:**
- 🔴 **Errors** - Exceptions, failures, crashes (voice: Adam)
- ⏱️  **Long Operations** - Commands taking 30+ seconds (voice: Bella)
- ✅ **Test Results** - Pytest, Jest, test pass/fail (voice: Emma)
- 🏗️  **Build Completions** - Webpack, Vite, builds (voice: Sarah)
- 🔀 **Git Operations** - Commits, pushes, merges (voice: George)

**Getting Started:**
```
# Enable automatic speech
/speech-config enable

# Test with a long operation
sleep 35 && echo "Done"

# Adjust sensitivity
/speech-config set min_priority 40  # Higher = fewer notifications
```


## Configuration

**ML Server:** http://ml-server:8001
**Text Limit:** 800 characters (optimal quality)
**Cache:** 100 entries, 1 hour TTL
**Audio Location:** ~/.cache/speech-mcp/

## Voices

- **af_bella** - American Female (warm, friendly)
- **af_sarah** - American Female (professional)
- **am_adam** - American Male (calm, measured)
- **am_michael** - American Male (energetic)
- **bf_emma** - British Female (refined)
- **bf_isabella** - British Female (elegant)
- **bm_george** - British Male (distinguished)
- **bm_lewis** - British Male (modern)

## Performance

- **Cache Hit:** ~0.01ms
- **Synthesis:** 200-500ms (GPU)
- **Audio Playback:** ~4ms

## Requirements

- ML server running on http://ml-server:8001
- Kokoro TTS service deployed
- Claude Code >= 1.0.0

## Version

1.0.0 - Full release with manual commands and automatic speech hooks

**Implemented:**
- ✅ Manual speech commands (/speak, /voices, /speech-status, /speech-config)
- ✅ Automatic speech hooks (PostToolUse, SessionStart, Stop)
- ✅ Quiet hours configuration (10 PM - 7 AM)
- ✅ Priority-based notifications (0-100 scoring)
- ✅ Event-driven speech automation (errors, tests, builds, git, long-running)
- ✅ Smart caching (10,000x speedup)
- ✅ GPU acceleration (RTX 5070 Ti)
- ✅ 8 voices (American and British, male and female)

**Future Enhancements:**
- Voice emotion control (pitch, tone variation)
- Custom voice cloning
- SSML support for rich speech formatting
- Webhook integrations (Slack, Discord notifications)

## Links

- **Repository:** https://github.com/flight505/Intelligent-speech
- **Author:** flight505
