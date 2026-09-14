"""CSS provider strings for Sticky's visual styling.

Provides CSS for:
- Manager window (minimal flat list with subtle blue accents)
- Note windows (5 pastel color variants)
- General widget styling
"""

# CSS for the manager window — original compact post-it list style
MANAGER_CSS = """
window.manager {
    background-color: #fff9d9;
    color: #3d3824;
    font-family: monospace;
    border-radius: 4px;
}

.manager > box {
    background-color: #fff9d9;
    border-radius: 4px;
}

.manager scrolledwindow,
.manager listview {
    background-color: #fff9d9;
    padding: 0;
}

.manager listview row {
    background-color: transparent;
    border: none;
    border-bottom: 1px solid rgba(61, 56, 36, 0.18);
    border-radius: 0;
    margin: 0;
    padding: 0;
}

.manager listview row:hover {
    background-color: rgba(255, 255, 255, 0.22);
}

.manager listview row:selected {
    background-color: rgba(190, 157, 35, 0.20);
    box-shadow: inset 3px 0 #8f7618;
}

.manager .title-label {
    font-size: 14px;
    color: #3d3824;
    font-weight: bold;
}

.manager .date-label {
    font-size: 12px;
    color: #756b43;
}

.manager .lock-button {
    background: transparent;
    border: none;
    color: #9a916f;
    font-size: 14px;
    padding: 2px 6px;
    border-radius: 4px;
}

.manager .lock-button:hover {
    color: #504a2c;
    background: rgba(190, 157, 35, 0.28);
}

.manager .lock-button.is-locked {
    color: #242012;
}

.manager button.delete-button,
.manager button.delete-button > label {
    background: transparent;
    border: none;
    color: #b84b4b;
    font-size: 14px;
    padding: 1px 5px;
    border-radius: 3px;
}

.manager button.delete-button:hover,
.manager button.delete-button:focus,
.manager button.delete-button:focus-visible {
    color: #8e3030;
    background: rgba(184, 75, 75, 0.12);
    outline: 1px solid rgba(142, 48, 48, 0.30);
    outline-offset: 0;
}

.manager button.delete-button:hover > label,
.manager button.delete-button:focus > label,
.manager button.delete-button:focus-visible > label {
    color: #8e3030;
}

.manager button.delete-button:active {
    color: #722323;
    background: rgba(184, 75, 75, 0.20);
}

.manager button.delete-button:active > label {
    color: #722323;
}

.manager button.add-button,
.manager button.add-button > label {
    min-width: 40px;
    min-height: 40px;
    background: #35a854;
    color: #fffbe0;
    border: none;
    font-size: 24px;
    font-weight: bold;
    padding: 0;
    border-radius: 999px;
}

.manager button.add-button:hover,
.manager button.add-button:focus,
.manager button.add-button:focus-visible {
    background: #2d9149;
    color: #ffffff;
    outline: 2px solid rgba(53, 168, 84, 0.35);
    outline-offset: 2px;
}

.manager button.add-button:hover > label,
.manager button.add-button:focus > label,
.manager button.add-button:focus-visible > label {
    color: #ffffff;
}

.manager button.add-button:active {
    background: #24763b;
    color: #ffffff;
}

.manager button.add-button:active > label {
    color: #ffffff;
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

.note-window > box {
    border-radius: 4px;
}

.note-yellow,
.note-yellow .toolbar-box,
.note-yellow textview {
    background-color: #fff9d9;
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
    min-width: 32px;
    min-height: 28px;
    padding: 0;
    margin: 0;
    border-radius: 5px;
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
    min-width: 32px;
    min-height: 28px;
    padding: 0;
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
.color-dropdown .color-option.color-yellow > label { color: #c29400; background-color: #fff9d9; }
.color-dropdown .color-option.color-green,
.color-dropdown .color-option.color-green > label { color: #168a3a; background-color: #c6f0c6; }
.color-dropdown .color-option.color-blue,
.color-dropdown .color-option.color-blue > label { color: #1769aa; background-color: #c6dff0; }
.color-dropdown .color-option.color-pink,
.color-dropdown .color-option.color-pink > label { color: #b52b7d; background-color: #f0c6e0; }
.color-dropdown .color-option.color-orange,
.color-dropdown .color-option.color-orange > label { color: #c45b18; background-color: #f0d0c0; }

.title-button {
    min-width: 32px;
    min-height: 28px;
    padding: 0;
}

.title-dropdown.popover {
    background-color: rgba(255, 255, 255, 0.98);
    border: 1px solid rgba(0, 0, 0, 0.14);
    border-radius: 10px;
    padding: 0;
}

.title-dropdown .title-option {
    min-width: 42px;
    min-height: 34px;
    padding: 0 4px;
    border: 1px solid rgba(0, 0, 0, 0.12);
    border-radius: 8px;
    background: rgba(0, 0, 0, 0.04);
}

.title-dropdown .title-option:hover,
.title-dropdown .title-option:focus {
    border-color: rgba(0, 0, 0, 0.42);
    background: rgba(0, 0, 0, 0.09);
}
"""

# Color definitions for programmatic use
PASTEL_COLORS = {
    "yellow": {"name": "Yellow", "css_class": "note-yellow", "hex": "#fff9d9"},
    "green": {"name": "Green", "css_class": "note-green", "hex": "#c6f0c6"},
    "blue": {"name": "Blue", "css_class": "note-blue", "hex": "#c6dff0"},
    "pink": {"name": "Pink", "css_class": "note-pink", "hex": "#f0c6e0"},
    "orange": {"name": "Orange", "css_class": "note-orange", "hex": "#f0d0c0"},
}

DEFAULT_COLOR = "yellow"
