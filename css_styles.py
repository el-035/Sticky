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

.color-dropdown button {
    font-family: monospace;
    font-size: 12px;
}

.color-dropdown popover {
    font-family: monospace;
    background-color: #fafafa;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 4px;
}

.color-dropdown popover button {
    padding: 4px 12px;
    border-radius: 3px;
    border: none;
    margin: 2px;
}

.color-dropdown popover button:hover {
    background-color: rgba(0, 0, 0, 0.1);
}
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
