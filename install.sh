#!/bin/bash
# Install Sticky as a desktop application
# Run this script to set up the app launcher and data directory

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_NAME="sticky"
DESKTOP_FILE="$SCRIPT_DIR/$APP_NAME.desktop"
LOCAL_APPS_DIR="$HOME/.local/share/applications"
LOCAL_DESKTOP="$LOCAL_APPS_DIR/$APP_NAME.desktop"

echo "=== Sticky Installer ==="
echo ""

# 1. Check Python and GTK dependencies
echo "1. Checking dependencies..."
python3 -c "
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gio', '2.0')
from gi.repository import Gtk
print('   GTK 4 Python bindings: OK')
" || {
    echo "   ERROR: GTK 4 Python bindings not found."
    echo "   Install with: sudo apt install python3-gi gir1.2-gtk-4.0"
    exit 1
}

# 2. Create notes data directory
echo "2. Creating notes directory..."
mkdir -p "$SCRIPT_DIR/notes"
echo "   $SCRIPT_DIR/notes/ created"

# 3. Install desktop launcher
echo "3. Installing desktop launcher..."
mkdir -p "$LOCAL_APPS_DIR"

# Update the desktop file with the correct path
sed "s|Exec=.*|Exec=python3 $SCRIPT_DIR/sticky.py|" "$DESKTOP_FILE" > "$LOCAL_DESKTOP"
chmod +x "$LOCAL_DESKTOP"

echo "   Desktop launcher installed to:"
echo "   $LOCAL_DESKTOP"

# 4. Update desktop database
echo "4. Updating application database..."
update-desktop-database "$LOCAL_APPS_DIR" 2>/dev/null || true
echo "   Done"

echo ""
echo "=== Installation complete! ==="
echo ""
echo "You can now find 'Sticky' in your app launcher/grid."
echo "Search for 'Sticky' or look under Utilities."
echo ""
echo "To uninstall, run:"
echo "  rm $LOCAL_DESKTOP"
echo "  (Your notes in $SCRIPT_DIR/notes/ will not be deleted)"
