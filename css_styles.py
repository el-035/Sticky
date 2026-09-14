"""CSS provider strings for Sticky's visual styling.

Provides CSS for:
- Manager window (modern dark gray with white text, matching the note aesthetic)
- Note windows (5 pastel color variants)
- General widget styling
"""

# CSS for the manager window — modern dark gray look with white text
MANAGER_CSS = """
window.manager {
    background-color: #2e2e2e;
    color: #f0f0f0;
    font-family: monospace;
}

.manager listview {
    background-color: #2e2e2e;
    color: #f0f0f0;
}

.manager listview row {
    padding: 8px 12px;
    border-bottom: 1px solid #404040;
    transition: background-color 150ms;
}

.manager listview row:hover {
    background-color: #3d3d3d;
}

.manager listview row:selected {
    background-color: #505050;
}

.manager .title-label {
    font-size: 14px;
    color: #f0f0f0;
    font-weight: bold;
}

.manager .date-label {
    font-size: 12px;
    color: #a0a0a0;
}

.manager .delete-button {
    background: none;
    border: none;
    color: #ff7777;
    font-size: 16px;
    padding: 2px 8px;
    border-radius: 4px;
}

.manager .delete-button:hover {
    color: #ff9999;
    background-color: #4a2a2a;
}

.manager .add-button {
    background: none;
    border: 1px solid #f0f0f0;
    color: #f0f0f0;
    font-size: 18px;
    padding: 4px 16px;
    border-radius: 4px;
}

.manager .add-button:hover {
    background-color: #4a4a4a;
}

.manager .color-dot {
    min-width: 10px;
    min-height: 10px;
    border-radius: 50%;
    margin-right: 8px;
}
"""

# CSS for note windows — 5 pastel color variants
NOTE_CSS = """
window.note-window {
    font-family: monospace;
    border-radius: 4px;
}

.note-yellow,
.note-yellow .toolbar-box,
.note-yellow textview {
    background-color: #fdf6c6;
}

.note-green,
.note-green .toolbar-box,
.note-green textview {
    background-color: #c6f0c6;
}

.note-blue,
.note-blue .toolbar-box,
.note-blue textview {
    background-color: #c6dff0;
}

.note-pink,
.note-pink .toolbar-box,
.note-pink textview {
    background-color: #f0c6e0;
}

.note-orange,
.note-orange .toolbar-box,
.note-orange textview {
    background-color: #f0d0c0;
}

.note-window textview {
    font-family: monospace;
    font-size: 13px;
    padding: 8px;
}

.note-window textview text {
    background-color: transparent;
}

.note-window .toolbar-box {
    font-family: monospace;
    font-size: 12px;
    padding: 4px 6px;
}

.note-window .toolbar-box button {
    font-family: monospace;
    font-size: 12px;
    padding: 2px 8px;
    margin: 0 2px;
    border-radius: 3px;
    background: rgba(0, 0, 0, 0.08);
    border: none;
}

.note-window .toolbar-box button:hover {
    background: rgba(0, 0, 0, 0.15);
}

.note-window .note-title-entry {
    font-family: monospace;
    font-size: 16px;
    font-weight: bold;
    background: transparent;
    border: none;
    border-bottom: 1px solid rgba(0, 0, 0, 0.15);
    padding: 4px 0;
    margin-left: 8px;
    margin-right: 8px;
}

.note-window .note-title-entry:focus {
    outline: none;
    border-bottom: 1px solid rgba(0, 0, 0, 0.35);
}

.note-window .color-button {
    min-width: 24px;
    min-height: 24px;
    padding: 2px 8px;
    font-size: 16px;
}

.note-window .color-button.color-yellow,
.note-window .color-button.color-yellow > label { color: #c29400; }
.note-window .color-button.color-green,
.note-window .color-button.color-green > label { color: #168a3a; }
.note-window .color-button.color-blue,
.note-window .color-button.color-blue > label { color: #1769aa; }
.note-window .color-button.color-pink,
.note-window .color-button.color-pink > label { color: #b52b7d; }
.note-window .color-button.color-orange,
.note-window .color-button.color-orange > label { color: #c45b18; }

.color-dropdown.popover {
    background-color: rgba(255, 255, 255, 0.98);
    border: 1px solid rgba(0, 0, 0, 0.14);
    border-radius: 10px;
    padding: 0;
}

.color-dropdown .color-option {
    min-width: 28px;
    min-height: 28px;
    padding: 0;
    border: 2px solid rgba(0, 0, 0, 0.12);
    border-radius: 999px;
    font-size: 16px;
    background: transparent;
}

.color-dropdown .color-option:hover,
.color-dropdown .color-option:focus {
    border-color: rgba(0, 0, 0, 0.48);
    box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.08);
}

.color-dropdown .color-option.color-yellow,
.color-dropdown .color-option.color-yellow > label { color: #c29400; background-color: #fdf6c6; }
.color-dropdown .color-option.color-green,
.color-dropdown .color-option.color-green > label { color: #168a3a; background-color: #c6f0c6; }
.color-dropdown .color-option.color-blue,
.color-dropdown .color-option.color-blue > label { color: #1769aa; background-color: #c6dff0; }
.color-dropdown .color-option.color-pink,
.color-dropdown .color-option.color-pink > label { color: #b52b7d; background-color: #f0c6e0; }
.color-dropdown .color-option.color-orange,
.color-dropdown .color-option.color-orange > label { color: #c45b18; background-color: #f0d0c0; }
"""

# Color definitions for programmatic use
PASTEL_COLORS = {
    "yellow": {"name": "Yellow", "css_class": "note-yellow", "hex": "#fdf6c6"},
    "green": {"name": "Green", "css_class": "note-green", "hex": "#c6f0c6"},
    "blue": {"name": "Blue", "css_class": "note-blue", "hex": "#c6dff0"},
    "pink": {"name": "Pink", "css_class": "note-pink", "hex": "#f0c6e0"},
    "orange": {"name": "Orange", "css_class": "note-orange", "hex": "#f0d0c0"},
}

DEFAULT_COLOR = "yellow"
