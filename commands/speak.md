---
name: speak
description: Manually trigger text-to-speech with customizable voice and speed
args:
  text:
    type: string
    description: The text to speak (max 800 characters)
    required: true
  voice:
    type: string
    description: Voice ID (af_bella, am_adam, bf_emma, bm_george, af_sarah, am_michael, bf_isabella, bm_lewis)
    required: false
    default: af_bella
  speed:
    type: number
    description: Speech speed multiplier (0.5-2.0)
    required: false
    default: 1.0
examples:
  - "/speak \"Build complete\""
  - "/speak \"Hello world\" --voice am_adam --speed 1.2"
  - "/speak \"Testing multiple voices\" --voice bf_emma"
---

Call the MCP tool `text_to_speech` with the following parameters:
- text: {text}
- voice: {voice}
- speed: {speed}
- format: "base64_wav"

The MCP tool will synthesize speech and automatically play the audio.

If the text is longer than 800 characters, warn the user and truncate it.

Available voices:
- American Female: af_bella (warm), af_sarah (professional)
- American Male: am_adam (calm), am_michael (confident)
- British Female: bf_emma (refined), bf_isabella (elegant)
- British Male: bm_george (distinguished), bm_lewis (articulate)

After calling the tool, briefly confirm what was spoken.
