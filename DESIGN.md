# Sticky — Design Document

## Overview

**Sticky** is a Linux desktop sticky-note application. It provides a central manager window to organize notes, and each note can open as an independent floating window. Built with GTK 4 + Python.

## Core Behavior

- **Manager window**: Compact list of all notes on the same yellow post-it background used by default notes, with dark monospace text.
- **Floating notes**: Each note opens as an independent window with a pastel-colored background covering the whole window (toolbar + editor). Monospace font.
- **App lifecycle**: The app runs while at least one window (manager or note) is open, and exits when the last window closes. Closing the manager window closes only the manager; any open note windows remain available.
- **Desktop launcher**: The installer adds a Sticky launcher to the user application menu. Pinning it to a dock or sidebar is a desktop environment setting.

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
  "locked": false,
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
| `locked` | Whether deletion is disabled for this note |
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
| `/t2 ... t2/` | Title level 2 | `/t2 Heading t2/` | **Heading** (medium font) |
| `/t3 ... t3/` | Title level 3 (smallest title) | `/t3 Heading t3/` | **Heading** (slightly larger than body) |

All title levels render in a font size larger than normal body text. `/t1` is the largest, `/t3` is the smallest title.

### Bullet Lists

- Typing `- ` (dash followed by a space) at the start of a line begins a bullet list. The `- ` marker stays visible (Markdown-style editing).
- Pressing Enter (newline) automatically inserts a bullet on the next line at the same indentation level.
- Pressing Tab on a bullet line indents it by four spaces; nested bullets continue at that indentation.
- Pressing Backspace on an empty indented bullet removes one four-space indentation level. At the top level, it removes the bullet prefix and exits list mode.
- Numbered lists are not supported (future feature).

### WYSIWYG Behavior

Formatting is WYSIWYG: as soon as you type `/b`, subsequent text appears bold until you close with `b/`. The markers are not visible in the rendered text.

## Toolbar (per floating note)

Each note window has a toolbar with:

| Icon/Button | Action |
|-------------|--------|
| **Bold** | Toggle `/b` formatting (also `Ctrl+B`) |
| **Italic** | Toggle `/i` formatting (also `Ctrl+I`) |
| **Title dropdown** | Select `/t1` through `/t3` (also `Ctrl+1` to `Ctrl+3`) |
| **Color picker** | Dropdown with 5 pastel color options |

The note window is closed with the window titlebar's close button or `Ctrl+W`.

All toolbar actions also have keyboard alternatives.

## Keyboard Shortcuts

### Local (when a Sticky window is focused)

| Shortcut | Action |
|----------|--------|
| `Ctrl+B` | Toggle bold formatting |
| `Ctrl+I` | Toggle italic formatting |
| `Ctrl+1` | Apply `/t1` title |
| `Ctrl+2` | Apply `/t2` title |
| `Ctrl+3` | Apply `/t3` title |
| `Ctrl+Plus` | Increase note size by a percentage increment |
| `Ctrl+W` | Close the focused note window |
| `Ctrl+Q` | Quit Sticky |
| `Ctrl+Alt+N` | Create and open a new note while Sticky is running |
| `Ctrl+drag` | Resize the note window with the mouse |

## Manager Window (List View)

- **Appearance**: Yellow post-it background, compact flat rows, dark monospace text, and simple controls.
- **Layout**: Vertical list of all notes.
- **Each list item shows**:
  - Explicit title if set; otherwise the first line of note content; otherwise the creation date + time (e.g., "2026-06-19 14:30:22")
  - Color indicator (small colored dot in the note's color)
  - Open/closed lock icon to toggle deletion protection
  - Delete icon (✕) on the right side — **instant deletion for unlocked notes, no confirmation**
- **Green "+" button**: Creates a new note from the bottom-right corner (also `Ctrl+Alt+N` while Sticky is running)
- **Window close / X**: Closes the manager window. The application exits after all note windows are closed as well.
- **Click on a row**: Opens the note as a floating window. If already open, brings the existing window to the front (no duplicates).
- **Search/filter/sort**: Not in v1 (future feature).
- **Grid view**: Not in v1 (future feature).
- **Settings button**: Not in v1 (future feature for default size, font, etc.).

## Note Window Behavior

- **Default size**: 320×320 pixels, resembling a physical post-it note.
- **Resizing**: Hold `Ctrl` while dragging in the note window to change its width and height. `Ctrl+Plus` increments the size by 15%.
- **Reopening**: Notes always reopen at the default size. Custom sizing is per-session only (does not persist across close/reopen).
- **Position**: The application tracks a cascade offset for new notes, but the desktop window manager controls their actual placement.
- **Always-on-top**: Use the window manager's "Always on Top" option (right-click the titlebar). No in-app pin control.
- **Close (window titlebar X or Ctrl+W)**: Closes the note window. The note remains in the manager list and can be reopened.
- **Lock (open/closed lock icon in list)**: Toggles deletion protection and persists with the note.
- **Delete (✕ icon in list)**: Permanently deletes an unlocked note and its JSON file. Locked notes cannot be deleted.

## Future Features (not in v1)

- Search/filter/sort in the manager
- Grid view option
- Settings panel (default note size, default font, etc.)
- Reminders/alarms on notes
- "Save as" — create a symlink/copy of a note to an arbitrary folder
- Numbered lists
- Dark/light mode toggle
- Note size/position memory across sessions

## App Icon

The bundled `sticky.svg` application icon was generated with ChatGPT.

## Technical Stack

- **Language**: Python 3
- **UI Toolkit**: GTK 4 (via PyGObject)
- **Data format**: JSON (one file per note)
- **Data location**: Single folder containing the app and all note JSON files
- **Target platform**: Linux (any distribution with GTK 4)
