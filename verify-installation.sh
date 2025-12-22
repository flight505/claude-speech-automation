#!/bin/bash
# Verification script for Speech Automation Plugin installation

echo "🔍 Speech Automation Plugin - Installation Verification"
echo "========================================================"
echo ""

PLUGIN_DIR="$HOME/.claude/plugins/speech-automation"
ERRORS=0

# Check plugin directory
if [ -d "$PLUGIN_DIR" ]; then
    echo "✅ Plugin directory exists: $PLUGIN_DIR"
else
    echo "❌ Plugin directory not found: $PLUGIN_DIR"
    ERRORS=$((ERRORS + 1))
fi

# Check plugin.json
if [ -f "$PLUGIN_DIR/.claude-plugin/plugin.json" ]; then
    echo "✅ Plugin manifest found"
else
    echo "❌ Plugin manifest missing: .claude-plugin/plugin.json"
    ERRORS=$((ERRORS + 1))
fi

# Check MCP server configuration
if [ -f "$PLUGIN_DIR/mcp-servers/speech-tts.json" ]; then
    echo "✅ MCP server configuration found"
else
    echo "❌ MCP server configuration missing"
    ERRORS=$((ERRORS + 1))
fi

# Check commands
echo ""
echo "Commands:"
for cmd in speak voices speech-status speech-config; do
    if [ -f "$PLUGIN_DIR/commands/$cmd.md" ]; then
        echo "  ✅ /$cmd"
    else
        echo "  ❌ /$cmd missing"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check hooks
echo ""
echo "Hooks:"
if [ -f "$PLUGIN_DIR/hooks/hooks.json" ]; then
    echo "  ✅ hooks.json configuration"
else
    echo "  ❌ hooks.json missing"
    ERRORS=$((ERRORS + 1))
fi

for hook in post_tool_use session_start stop; do
    if [ -f "$PLUGIN_DIR/hooks/$hook.py" ]; then
        if [ -x "$PLUGIN_DIR/hooks/$hook.py" ]; then
            echo "  ✅ $hook.py (executable)"
        else
            echo "  ⚠️  $hook.py (not executable - run: chmod +x)"
            ERRORS=$((ERRORS + 1))
        fi
    else
        echo "  ❌ $hook.py missing"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check common utilities
echo ""
echo "Hook Utilities:"
for util in config_loader priority_scorer speech_trigger __init__; do
    if [ -f "$PLUGIN_DIR/hooks/common/$util.py" ]; then
        echo "  ✅ common/$util.py"
    else
        echo "  ❌ common/$util.py missing"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check configuration
echo ""
if [ -f "$PLUGIN_DIR/config.yaml" ]; then
    echo "✅ Configuration file: config.yaml"

    # Check if automation is enabled
    if grep -q "^enabled: true" "$PLUGIN_DIR/config.yaml"; then
        echo "  ℹ️  Automatic speech: ENABLED"
    else
        echo "  ℹ️  Automatic speech: DISABLED (use /speech-config enable)"
    fi
else
    echo "❌ Configuration file missing"
    ERRORS=$((ERRORS + 1))
fi

# Check documentation
echo ""
echo "Documentation:"
for doc in README.md TESTING.md; do
    if [ -f "$PLUGIN_DIR/$doc" ]; then
        echo "  ✅ $doc"
    else
        echo "  ⚠️  $doc missing"
    fi
done

# Summary
echo ""
echo "========================================================"
if [ $ERRORS -eq 0 ]; then
    echo "✅ Installation verified successfully!"
    echo ""
    echo "Next steps:"
    echo "  1. Restart Claude Code to load the plugin"
    echo "  2. Test with: /speak \"Hello from speech automation\""
    echo "  3. Enable automation: /speech-config enable"
    echo "  4. See TESTING.md for comprehensive test guide"
else
    echo "❌ Installation incomplete - $ERRORS errors found"
    echo ""
    echo "Please review the errors above and fix missing files."
fi

exit $ERRORS
