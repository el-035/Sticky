#!/usr/bin/env python3
"""Sticky — A Linux desktop sticky-note application.

Entry point: StickyApp (Gtk.Application subclass).
Manages app lifecycle, global actions, and coordinates
the manager window and floating note windows.
"""

import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gio", "2.0")
gi.require_version("GLib", "2.0")

from gi.repository import Gtk, Gio, GLib  # noqa: E402

from typing import Optional  # noqa: E402

from note_store import NoteStore  # noqa: E402
from note_model import NoteModel  # noqa: E402


class StickyApp(Gtk.Application):
    """Main application class for Sticky.

    Owns the NoteStore, ManagerWindow (singleton), and tracks
    all open NoteWindows. Handles lifecycle (hold/release) so
    global shortcuts work even when the manager is hidden.
    """

    def __init__(self):
        super().__init__(
            application_id="com.sticky.notes",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
        )
        self.note_store: NoteStore = None
        self.manager_window = None
        self.open_windows: dict[str, "NoteWindow"] = {}  # note_id -> NoteWindow

        # Action to fire on activation after a command-line invocation.
        # Used for --new-note so the action runs after the app
        # has finished registering as the primary instance.
        self._pending_action: Optional[str] = None

        # Command-line options used for system-level global shortcuts.
        # These are handled in do_command_line and forwarded to the running
        # primary instance if the app is already open.
        self.add_main_option(
            "new-note",
            0,
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Create and open a new note",
            None,
        )

    def do_command_line(self, command_line):
        """Handle command-line invocations forwarded to the primary instance.

        --new-note creates a new note without opening the manager.
        A plain invocation (no options) activates/presents the manager.
        """
        options = command_line.get_options_dict()
        options = options.end().unpack() if options else {}
        args = command_line.get_arguments()

        want_new_note = options.get("new-note", False) or "--new-note" in args

        if want_new_note:
            self._pending_action = "new-note"
            self.activate()
            return 0

        # Default: present the manager window.
        self.activate()
        return 0

    def do_startup(self):
        """Initialize app: hold to prevent exit, create store, setup actions."""
        Gtk.Application.do_startup(self)

        # The app runs only while at least one window is open. With system-level
        # shortcuts starting the app on demand, there is no need to keep it alive
        # in the background when all windows are closed.
        self.note_store = NoteStore()
        self._setup_actions()
        self._setup_global_shortcuts()

    def do_activate(self):
        """Create or present the manager window.

        Called on first launch, dock icon click, D-Bus activation, or from
        do_command_line when a command-line option needs to trigger an action.
        """
        if self._pending_action:
            action = self._pending_action
            self._pending_action = None
            self.activate_action(action, None)
            return

        if self.manager_window is None:
            # Import here to avoid circular dependency
            from notes_manager import ManagerWindow

            self.manager_window = ManagerWindow(self)
        else:
            self.manager_window.present()

    def _setup_actions(self):
        """Register GActions for the app."""
        # New note action
        new_action = Gio.SimpleAction.new("new-note", None)
        new_action.connect("activate", self._on_new_note)
        self.add_action(new_action)

        # Quit action
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self._on_quit)
        self.add_action(quit_action)

    def _setup_global_shortcuts(self):
        """Register keyboard shortcuts.

        Local accelerators work when any Sticky window has focus. True global
        shortcuts are configured by the user in GNOME Settings using the
        command-line options --new-note.
        """
        # Local accelerators.
        self.set_accels_for_action("app.new-note", ["<Control><Alt>n"])
        self.set_accels_for_action("app.quit", ["<Control>q"])

    def _on_new_note(self, action, param):
        """Create a new note and open it immediately."""
        note = self.note_store.create()
        self._open_note_window(note)

        # Also add to manager list if visible
        if self.manager_window is not None:
            self.manager_window.add_note_to_list(note)

    def _on_quit(self, action, param):
        """Truly exit the application."""
        # Close all open note windows
        for note_id, window in list(self.open_windows.items()):
            window.destroy()
        self.open_windows.clear()

        # Destroy manager window
        if self.manager_window is not None:
            self.manager_window.destroy()
            self.manager_window = None

        self.quit()

    def on_note_activated(self, note_id: str):
        """Handle a note being clicked in the manager list.

        If the note is already open, present its window.
        Otherwise, load and open it.
        """
        if note_id in self.open_windows:
            self.open_windows[note_id].present()
            return

        note = self.note_store.get(note_id)
        if note is None:
            print(f"Warning: note {note_id} not found on disk")
            return

        self._open_note_window(note)

    def on_note_deleted(self, note_id: str):
        """Handle a note being deleted from the manager list.

        Closes the note window if open, then removes the JSON file.
        """
        if note_id in self.open_windows:
            self.open_windows[note_id].destroy()
            del self.open_windows[note_id]

        self.note_store.delete(note_id)

    def _open_note_window(self, note: NoteModel):
        """Create and show a floating NoteWindow for the given note."""
        from note_window import NoteWindow

        window = NoteWindow(self, note)
        self.open_windows[note.id] = window
        window.present()

    def on_note_window_closed(self, note_id: str):
        """Called by NoteWindow when its X button is clicked."""
        if note_id in self.open_windows:
            del self.open_windows[note_id]


def main():
    """Entry point."""
    app = StickyApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
