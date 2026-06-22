# Sticky — Post-It Note App for Linux

A Linux desktop sticky-note application built with GTK 4 + Python. Notes are stored as JSON files in a single folder. Features a modern dark gray manager window and pastel-colored floating note windows with custom inline formatting markup.

## Key Design Decisions

- GTK 4 + Python (PyGObject)
- One JSON file per note, instant auto-save on every keystroke
- Notes have an optional dedicated **title** field shown at the top of each note and in the manager list
- Custom formatting syntax: `/b bold b/`, `/i italic i/`, `/t1`–`/t4` for titles
- Bullet lists via `- ` (dash + space) at line start, auto-continues on Enter; `- ` marker stays visible (Markdown-style)
- 5 pastel colors color the entire note window: yellow (default), green, blue, pink/purple, orange/red
- WYSIWYG formatting markers hidden, text styled immediately
- System shortcut (Ctrl+Alt+N new note) configured in GNOME Settings runs `python3 sticky.py --new-note`
- Local shortcut Ctrl+W closes a focused note window
- Always-on-top is handled by the window manager (right-click titlebar → Always on Top); no in-app pin button
- App quits when the last window is closed (manager or note)
- Notes always reopen at default post-it square size
- Delete is instant, no confirmation

## Project Structure

```
postit/
├── DESIGN.md          # Full design specification
├── CLAUDE.md          # This file — project context for Claude Code
├── sticky.py          # Main application entry point (to be created)
├── notes/             # Directory where note JSON files are stored
│   ├── 20260619-143022.json
│   └── ...
└── requirements.txt   # Python dependencies (to be created)
```

## Dependencies

- Python 3
- PyGObject (GTK 4 Python bindings)
- pycairo (optional; for custom `Gtk.DrawingArea` draw functions)
- On Ubuntu: `sudo apt install python3-gi gir1.2-gtk-4.0 python3-gi-cairo`

See DESIGN.md for the complete specification.
