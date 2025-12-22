---
name: voices
description: List all available voices with samples
args:
  play-samples:
    type: boolean
    description: Play a sample phrase with each voice
    required: false
    default: false
examples:
  - "/voices"
  - "/voices --play-samples"
---

Call the MCP tool `list_voices` to get all available voices.

Display the voices in an organized format:

**🇺🇸 American Voices:**
- **Female:**
  - af_bella - Bella (warm, friendly)
  - af_sarah - Sarah (professional, clear)
- **Male:**
  - am_adam - Adam (calm, reassuring)
  - am_michael - Michael (confident, articulate)

**🇬🇧 British Voices:**
- **Female:**
  - bf_emma - Emma (refined, elegant)
  - bf_isabella - Isabella (sophisticated, polished)
- **Male:**
  - bm_george - George (distinguished, authoritative)
  - bm_lewis - Lewis (articulate, warm)

For each voice, show a sample command like:
`/speak "Hello, I'm Bella" --voice af_bella`

If the `--play-samples` flag is provided, call the `text_to_speech` tool for each voice with the text:
"Hello, I am [voice_name]"

Use speed 1.0 for all samples and play them sequentially.

At the end, show the hint: "Use /speak with --voice parameter to select a voice"
