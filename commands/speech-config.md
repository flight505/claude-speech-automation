---
name: speech-config
description: Configure automatic speech automation settings
args:
  action:
    type: string
    description: Action (enable, disable, set) or leave empty to view config
    required: false
  key:
    type: string
    description: Config key to set (use dot notation like events.errors.enabled)
    required: false
  value:
    type: string
    description: Value to set
    required: false
examples:
  - "/speech-config"
  - "/speech-config enable"
  - "/speech-config disable"
  - "/speech-config set min_priority 50"
  - "/speech-config set events.errors.enabled false"
---

Load configuration from: ~/.claude/plugins/speech-automation/config.yaml

**If no action provided (view mode):**

Display current configuration:

**🔧 Speech Automation Configuration**

Status: [✅ Enabled or ❌ Disabled]
Min Priority: [value] (0-100 scale)
Rate Limit: [value] seconds
Debounce: [value] ms

**Quiet Hours:**
- Enabled: [yes/no]
- Hours: [start_hour]:00 - [end_hour]:00
- Behavior: [disable/reduce]
- Priority Multiplier: [value]

**Events:**
- Long Running: [enabled], voice: [voice]
- Errors: [enabled], voice: [voice]
- Test Results: [enabled], pass: [speak_on_pass], fail: [speak_on_fail], voice: [voice]
- Build Completion: [enabled], voice: [voice]
- Git Operations: [enabled], voice: [voice]

Show hint: "Edit config: ~/.claude/plugins/speech-automation/config.yaml"

**If action is "enable":**
- Load YAML, set `enabled: true`, save file
- Confirm: "✅ Automatic speech enabled"

**If action is "disable":**
- Load YAML, set `enabled: false`, save file
- Confirm: "❌ Automatic speech disabled"

**If action is "set":**
- Parse {key} using dot notation (e.g., "events.errors.enabled")
- Navigate nested structure by splitting on dots
- Convert {value} to appropriate type:
  - "true"/"false" → boolean
  - Numeric string → int or float
  - Otherwise → string
- Update YAML and save
- Confirm: "✅ Set {key} = {value}"

After any change, remind: "Changes take effect immediately. No restart required."

Show priority score guide:
- 0-20: Low priority
- 21-50: Medium priority
- 51-80: High priority
- 81-100: Critical priority

Common config keys for reference:
- enabled, min_priority, rate_limit_seconds
- events.errors.enabled, events.errors.voice
- events.test_results.speak_on_pass
- quiet_hours.start_hour, quiet_hours.behavior
