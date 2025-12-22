---
name: speech-status
description: Check speech system status including MCP server and ML server health
examples:
  - "/speech-status"
---

Call the MCP tool `get_tts_status` to retrieve comprehensive system status.

Display the information in this format:

**🔊 Speech Automation Status**

**MCP Server:**
- Status: [Show if running/healthy]
- Uptime: [If available in response]

**ML Server:**
- URL: [ml_server_url from status]
- Model: Kokoro TTS 82M
- Health: [healthy/unhealthy based on response]
- GPU: [Available/Not Available]
- GPU Memory: [If available]

**Cache Statistics:**
- Entries: [current/max]
- Hits: [number]
- Misses: [number]
- Hit Rate: [percentage]
- Performance insight based on hit rate:
  - >70%: "⚡ Excellent (cache optimized)"
  - >40%: "✅ Good"
  - Otherwise: "⚠️ Cache warming up"

**Configuration:**
- Text Limit: 800 characters
- Cache Size: 100 entries
- Cache TTL: 1 hour
- Audio Format: WAV (24kHz, 16-bit mono)
- Location: ~/.cache/speech-mcp/

**Performance Metrics:**
- Cache Hit: ~0.01ms (10,000x faster)
- Synthesis: 200-500ms (GPU accelerated)
- Audio Playback: ~4ms overhead

If ML server is unreachable, show helpful message:
"⚠️ ML server not responding. Check if service is running on http://ml-server:8001"

At the end, show tips:
- "Use /voices to see available voices"
- "Use /speak to test synthesis"
- "Repeated phrases are cached automatically"
