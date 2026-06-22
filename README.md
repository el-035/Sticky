# Sticky

A simple, lightweight sticky-note app for Linux. Jot things down, keep them visible, never lose a thought.

![Sticky](placeholder-for-screenshot.png)

## How It Looks

- **Manager window**: Retro terminal style — black background, green text. Lists all your notes in one place.
- **Notes**: Pastel-colored floating squares, like real post-its. Yellow by default, four other colors available.

## Installation

### Requirements

- Linux (any distribution with GTK 4)
- Python 3

### Install Dependencies

**Ubuntu/Debian:**
```bash
sudo apt install python3-gi gir1.2-gtk-4.0
```

**Fedora:**
```bash
sudo dnf install python3-gobject gtk4
```

**Arch:**
```bash
sudo pacman -S python-gobject gtk4
```

### Run Stick

```bash
cd sticky/
python3 sticky.py
```

Pin Sticky to your dock/sidebar for quick access.

## Usage

### Creating Notes

| Action | How |
|--------|-----|
| **New note from manager** | Click the **+** button in the manager window |
| **New note from anywhere** | Press `Ctrl+Alt+N` (works even when Stick is in the background!) |

### Managing Notes

- **Open a note**: Click it in the manager list. If it's already open, it jumps to the front.
- **Close a note**: Click the **X** button on the note's toolbar. The note stays in your list.
- **Delete a note permanently**: Click the **trash icon** next to the note in the manager list. Instant — no confirmation.
- **Quit Stick entirely**: Click the **Quit** button in the manager window.

> **Tip**: Closing the manager window just hides it — Sticky keeps running so `Ctrl+Alt+N` always works. Click the dock icon to bring it back.

### Formatting Text

Sticky uses simple inline markers. As you type, text renders styled instantly — the markers disappear.

| You type | You see |
|----------|---------|
| `/b important b/` | **important** (bold) |
| `/i subtle i/` | *subtle* (italic) |
| `/t1 Big Title t1/` | **Big Title** (largest heading) |
| `/t2 Heading t2/` | **Heading** (large) |
| `/t3 Heading t3/` | **Heading** (medium) |
| `/t4 Heading t4/` | **Heading** (small heading) |

You can also use keyboard shortcuts while typing:
- `Ctrl+B` — bold
- `Ctrl+I` — italic
- `Ctrl+1` to `Ctrl+4` — title levels 1 through 4

### Making Lists

Type `-` at the start of a line to begin a bullet list:
```
- Milk
- Bread
- Eggs
```

Press **Enter** at the end of a line — a new `-` appears automatically. To exit the list, delete the `-` on an empty bullet line.

### Changing Note Color

Click the **color icon** on the note's toolbar. A dropdown shows five pastel colors:

| Color | Vibe |
|-------|------|
| Yellow | Default, classic post-it |
| Green | Go, tasks, done |
| Blue | Info, reference |
| Pink/Purple | Personal, ideas |
| Orange/Red | Urgent, important |

### Keeping Notes Visible (Always on Top)

- Click the **pin icon** on the note's toolbar to toggle it on/off.
- Or press `Ctrl+Alt+P` from anywhere to toggle pin for all open notes.

When pinned, the note stays above other windows — great for reference info while working in another app.

### Resizing Notes

- **Mouse**: Hold `Ctrl` and drag any corner of the note.
- **Keyboard**: `Ctrl+Plus` increases the note size by a step.

Notes always reopen at the default post-it square size. Custom sizing is temporary (per session).

### Finding Your Notes

All notes are stored as JSON files in the `notes/` folder next to the app. To back up your notes, just copy that folder.

## Keyboard Shortcuts Cheat Sheet

### Global (work anywhere)

| Shortcut | Action |
|----------|--------|
| `Ctrl+Alt+N` | New note |
| `Ctrl+Alt+P` | Toggle always-on-top |

### While Typing in a Note

| Shortcut | Action |
|----------|--------|
| `Ctrl+B` | Bold |
| `Ctrl+I` | Italic |
| `Ctrl+1` | Title level 1 |
| `Ctrl+2` | Title level 2 |
| `Ctrl+3` | Title level 3 |
| `Ctrl+4` | Title level 4 |
| `Ctrl+Plus` | Enlarge note |

## Data & Privacy

Everything lives in one folder on your computer. No cloud, no accounts, no internet needed. Your notes are plain JSON files — you can open them in any text editor.
