# Sticky — Post-It Note App for Linux

A Linux desktop sticky-note application built with GTK 4 + Python. Notes are stored as JSON files in a single folder. Features a modern dark gray manager window and pastel-colored floating note windows with custom inline formatting markup.

## Key Design Decisions

- GTK 4 + Python (PyGObject)
- One JSON file per note, instant auto-save on every keystroke
- Notes have an optional dedicated **title** field shown at the top of each note and in the manager list
- Custom formatting syntax: `/b bold b/`, `/i italic i/`, `/t1`–`/t3` for titles
- Bullet lists via `- ` (dash + space) at line start, auto-continue on Enter, and four-space indentation with Tab, and Backspace outdents empty nested bullets; `- ` marker stays visible (Markdown-style)
- 5 pastel colors color the entire note window: yellow (default), green, blue, pink/purple, orange/red
- WYSIWYG formatting markers hidden, text styled immediately
- Local shortcut Ctrl+Alt+N creates a new note while Sticky is running
- Local shortcut Ctrl+W closes a focused note window
- Always-on-top is handled by the window manager (right-click titlebar → Always on Top); no in-app pin button
- App quits when the last window is closed (manager or note)
- Notes always reopen at default post-it square size
- Delete is instant for unlocked notes, no confirmation
- Notes can be locked from the manager to prevent accidental deletion

## Project Structure

```
postit/
├── DESIGN.md          # Full design specification
├── AGENTS.md          # Project instructions and context for Codex
├── sticky.py          # Main application entry point
├── note_model.py      # Note data model
├── note_store.py      # JSON persistence
├── notes_manager.py   # Manager window
├── note_window.py     # Floating note windows
├── wysiwyg_editor.py  # GTK text editor
├── formatting.py      # Inline formatting engine
├── css_styles.py      # GTK CSS definitions
├── notes/             # Directory where note JSON files are stored
│   ├── 20260619-143022.json
│   └── ...
└── requirements.txt   # Dependency notes
```

## Dependencies

- Python 3
- PyGObject (GTK 4 Python bindings)
- On Ubuntu: `sudo apt install python3-gi gir1.2-gtk-4.0`

See DESIGN.md for the complete specification.
