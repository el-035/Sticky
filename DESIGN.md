# Sticky — Design Document

## Overview

**Sticky** is a Linux desktop sticky-note application. It provides a central manager window to organize notes, and each note can open as an independent floating window. Built with GTK 4 + Python.

## Core Behavior

- **Manager window**: List view of all notes. Black background, bright green text, monospace font (retro terminal aesthetic).
- **Floating notes**: Each note opens as an independent window with a pastel-colored background covering the whole window (toolbar + editor). Monospace font.
- **App lifecycle**: The app runs only while at least one window (manager or note) is open. Closing the manager window quits the app. Closing the last note window also quits the app. System shortcuts (`python3 sticky.py --new-note`) start the app on demand when needed.
- **Dock icon**: Added to the Ubuntu dock/sidebar as a favorite app for quick access.

## Note Storage

- Each note is stored as a **single JSON file** in the app's data folder.
- The folder *is* the database — portable, human-readable, easy to back up.
- Auto-save is **instant** — every keystroke triggers a save.

### JSON Structure

```json
{
  "id": "20260619-143022",
  "title": "Shopping List",
  "content": "- Milk\n- Bread\n/b Don't forget the bread! b/",
  "color": "yellow",
  "created": "2026-06-19 14:30:22",
  "modified": "2026-06-19 15:12:08"
}
```

| Field | Description |
|-------|-------------|
| `id` | Unique identifier (timestamp-based on creation) |
| `title` | Optional explicit note title, shown in the manager list |
| `content` | Raw note text including formatting markup |
| `color` | One of: `yellow`, `green`, `blue`, `pink`, `orange` |
| `created` | Creation timestamp |
| `modified` | Last modification timestamp |

## Note Colors

Five pastel colors color the entire note window (background, toolbar, and editor area). Selectable via a dropdown icon on each note's toolbar:

1. **Yellow** (default for new notes)
2. **Green**
3. **Blue**
4. **Pink/Purple**
5. **Orange/Red**

## Text Formatting

### Inline Markup Syntax

Markers act as toggles — text renders styled between the open and close markers. The markers themselves are hidden in the rendered view.

| Syntax | Effect | Example Input | Rendered Result |
|--------|--------|---------------|-----------------|
| `/b ... b/` | Bold | `/b hello b/` | **hello** |
| `/i ... i/` | Italic | `/i hello i/` | *hello* |
| `/t1 ... t1/` | Title level 1 (largest) | `/t1 Heading t1/` | **Heading** (large font) |
| `/t2 ... t2/` | Title level 2 | `/t2 Heading t2/` | **Heading** (medium-large font) |
| `/t3 ... t3/` | Title level 3 | `/t3 Heading t3/` | **Heading** (medium font) |
| `/t4 ... t4/` | Title level 4 (smallest title) | `/t4 Heading t4/` | **Heading** (slightly larger than body) |

All title levels render in a font size larger than normal body text. `/t1` is the largest, `/t4` is the smallest title.

### Bullet Lists

- Typing `- ` (dash followed by a space) at the start of a line begins a bullet list. The `- ` marker stays visible (Markdown-style editing).
- Pressing Enter (newline) automatically inserts `- ` on the next line and places the cursor after it, continuing the list.
- Pressing Backspace on an empty bullet line (`- ` with no content) removes the bullet prefix and exits list mode.
- Numbered lists are not supported (future feature).

### WYSIWYG Behavior

Formatting is WYSIWYG: as soon as you type `/b`, subsequent text appears bold until you close with `b/`. The markers are not visible in the rendered text.

## Toolbar (per floating note)

Each note window has a toolbar with:

| Icon/Button | Action |
|-------------|--------|
| **Bold** | Toggle `/b` formatting (also `Ctrl+B`) |
| **Italic** | Toggle `/i` formatting (also `Ctrl+I`) |
| **Title dropdown** | Select `/t1` through `/t4` (also `Ctrl+1` to `Ctrl+4`) |
| **Color picker** | Dropdown with 5 pastel color options |

The note window is closed with the window titlebar's close button or `Ctrl+W`.

All toolbar actions also have keyboard alternatives.

## Keyboard Shortcuts

### Global (configured in GNOME Settings, works from any app)

| Shortcut | Command | Action |
|----------|---------|--------|
| `Ctrl+Alt+N` | `python3 /home/el/sideProjects/postit/sticky.py --new-note` | Create and open a new floating note instantly |

### Local (only when a Stick note window is focused)

| Shortcut | Action |
|----------|--------|
| `Ctrl+B` | Toggle bold formatting |
| `Ctrl+I` | Toggle italic formatting |
| `Ctrl+1` | Apply `/t1` title |
| `Ctrl+2` | Apply `/t2` title |
| `Ctrl+3` | Apply `/t3` title |
| `Ctrl+4` | Apply `/t4` title |
| `Ctrl+Plus` | Increase note size by a percentage increment |
| `Ctrl+W` | Close the focused note window |
| `Ctrl+drag corner` | Resize note window with mouse |

## Manager Window (List View)

- **Appearance**: Dark gray background, white text, monospace font.
- **Layout**: Vertical list of all notes.
- **Each list item shows**:
  - Explicit title if set; otherwise the first line of note content; otherwise the creation date + time (e.g., "2026-06-19 14:30:22")
  - Color indicator (small colored dot in the note's color)
  - Delete icon (✕) on the right side — **instant deletion, no confirmation**
- **"+" button**: Creates a new note (also `Ctrl+Alt+N`)
- **Window close / X**: Quits the application entirely
- **Click on a row**: Opens the note as a floating window. If already open, brings the existing window to the front (no duplicates).
- **Search/filter/sort**: Not in v1 (future feature).
- **Grid view**: Not in v1 (future feature).
- **Settings button**: Not in v1 (future feature for default size, font, etc.).

## Note Window Behavior

- **Default size**: Small square, resembling a physical post-it note.
- **Resizing**: 
  - `Ctrl + mouse drag` from any corner
  - `Ctrl+Plus` increments size by a percentage
- **Reopening**: Notes always reopen at the default size. Custom sizing is per-session only (does not persist across close/reopen).
- **Position**: New notes cascade slightly offset so they don't stack exactly on top of each other.
- **Always-on-top**: Use the window manager's "Always on Top" option (right-click the titlebar). No in-app pin control.
- **Close (window titlebar X or Ctrl+W)**: Closes the note window. The note remains in the manager list and can be reopened.
- **Delete (✕ icon in list)**: Permanently deletes the note and its JSON file. Instant, no confirmation dialog.

## Future Features (not in v1)

- Search/filter/sort in the manager
- Grid view option
- Settings panel (default note size, default font, etc.)
- Reminders/alarms on notes
- "Save as" — create a symlink/copy of a note to an arbitrary folder
- Numbered lists
- Dark/light mode toggle
- Note size/position memory across sessions

## Technical Stack

- **Language**: Python 3
- **UI Toolkit**: GTK 4 (via PyGObject)
- **Data format**: JSON (one file per note)
- **Data location**: Single folder containing the app and all note JSON files
- **Target platform**: Linux (any distribution with GTK 4)
