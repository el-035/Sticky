"""WysiwygEditor — a Gtk.TextView subclass with real-time WYSIWYG formatting.

Handles:
- Real-time formatting via FormattingEngine on every text change
- Bullet list auto-continue on Enter, exit on BackSpace
- Toolbar action methods (toggle bold/italic, apply title)
- Content extraction (raw markup for save, visible text for preview)
"""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("GLib", "2.0")

from gi.repository import Gtk, Gdk, GLib  # noqa: E402

from formatting import FormattingEngine  # noqa: E402


class WysiwygEditor(Gtk.TextView):
    """A text editor that renders custom markup as WYSIWYG formatted text.

    Markers like /b, /i, /t1-t3 are hidden and their content styled.
    Bullet lines starting with '- ' have the prefix hidden.
    """

    def __init__(self):
        super().__init__()

        # Create the formatting engine
        self.engine = FormattingEngine()

        # Configure the buffer
        buffer = self.get_buffer()
        self.engine.setup_tags(buffer)

        # Monospace font
        self.set_monospace(True)

        # Wrap text at word boundaries
        self.set_wrap_mode(Gtk.WrapMode.WORD)

        # Padding
        self.set_top_margin(8)
        self.set_bottom_margin(8)
        self.set_left_margin(8)
        self.set_right_margin(8)

        # Connect buffer changes → formatting scan
        buffer.connect("changed", self._on_buffer_changed)

        # Key controller for Enter and BackSpace (bullet list handling)
        key_controller = Gtk.EventControllerKey.new()
        key_controller.connect("key-pressed", self._on_key_pressed)
        self.add_controller(key_controller)

        # Local formatting shortcuts (Ctrl+B, Ctrl+I, Ctrl+1-3)
        self._setup_local_shortcuts()

        # Callback for external save notification (set by NoteWindow)
        self.on_content_changed_callback = None

    def _setup_local_shortcuts(self):
        """Register local keyboard shortcuts for formatting.

        These only work when this editor has focus.
        """
        ctrl = Gtk.ShortcutController()
        ctrl.set_scope(Gtk.ShortcutScope.LOCAL)

        # Ctrl+B → bold
        trigger = Gtk.ShortcutTrigger.parse_string("<Control>b")
        action = Gtk.CallbackAction.new(lambda w, e: self.toggle_bold())
        ctrl.add_shortcut(Gtk.Shortcut.new(trigger=trigger, action=action))

        # Ctrl+I → italic
        trigger = Gtk.ShortcutTrigger.parse_string("<Control>i")
        action = Gtk.CallbackAction.new(lambda w, e: self.toggle_italic())
        ctrl.add_shortcut(Gtk.Shortcut.new(trigger=trigger, action=action))

        # Ctrl+1 through Ctrl+3 → titles
        for level in range(1, 4):
            trigger = Gtk.ShortcutTrigger.parse_string(f"<Control>{level}")
            lvl = level  # capture for closure
            action = Gtk.CallbackAction.new(lambda w, e, n=lvl: self.apply_title(n))
            ctrl.add_shortcut(Gtk.Shortcut.new(trigger=trigger, action=action))

        # Ctrl+plus → enlarge
        trigger = Gtk.ShortcutTrigger.parse_string("<Control>plus")
        action = Gtk.CallbackAction.new(lambda w, e: self.enlarge())
        ctrl.add_shortcut(Gtk.Shortcut.new(trigger=trigger, action=action))

        # Ctrl+equal (= is on the same key as + without shift)
        trigger = Gtk.ShortcutTrigger.parse_string("<Control>equal")
        action = Gtk.CallbackAction.new(lambda w, e: self.enlarge())
        ctrl.add_shortcut(Gtk.Shortcut.new(trigger=trigger, action=action))

        self.add_controller(ctrl)

    def _on_buffer_changed(self, buffer):
        """Called on every text change. Re-applies formatting and triggers save."""
        # Re-apply formatting around the cursor
        self.engine.scan_around_cursor(buffer)

        # Notify external callback (auto-save)
        if self.on_content_changed_callback:
            self.on_content_changed_callback()

    def _on_key_pressed(self, controller, keyval, keycode, state):
        """Handle special keys for bullet list behavior.

        Enter on a bullet line → continue at the same indentation level.
        Tab on a bullet line → indent it by four spaces.
        BackSpace on an empty nested bullet → outdent one level; at the top level, delete the bullet prefix.
        """
        buffer = self.get_buffer()

        if keyval == Gdk.KEY_Return or keyval == Gdk.KEY_KP_Enter:
            if self.engine.is_bullet_line(buffer):
                # Insert newline + '- ' and position cursor after it, then hide it.
                self.engine.insert_bullet_on_enter(buffer)
                self.engine.scan_around_cursor(buffer)
                return True  # We handled Enter; do not run the default handler

        elif keyval == Gdk.KEY_Tab or keyval == Gdk.KEY_ISO_Left_Tab:
            if self.engine.indent_bullet(buffer, spaces=4):
                self.engine.scan_around_cursor(buffer)
                return True  # We handled Tab

        elif keyval == Gdk.KEY_BackSpace:
            # Outdent an empty nested bullet before deleting a top-level bullet.
            if self.engine.outdent_empty_bullet(buffer, spaces=4):
                self.engine.scan_around_cursor(buffer)
                return True  # We handled BackSpace as an outdent
            # Check if current line is an empty bullet
            if self.engine.delete_empty_bullet(buffer):
                self.engine.scan_around_cursor(buffer)
                return True  # We handled it, prevent default

        return False  # Let default handler process the key

    # --- Toolbar action methods ---

    def toggle_bold(self):
        """Insert /b ... b/ markers around selection or at cursor."""
        buffer = self.get_buffer()
        self.engine.insert_markers(buffer, "/b", "b/")
        self.engine.scan_around_cursor(buffer)

    def toggle_italic(self):
        """Insert /i ... i/ markers around selection or at cursor."""
        buffer = self.get_buffer()
        self.engine.insert_markers(buffer, "/i", "i/")
        self.engine.scan_around_cursor(buffer)

    def apply_title(self, level: int):
        """Insert /tN ... tN/ markers around selection or at cursor.

        Args:
            level: Title level 1-3.
        """
        if level < 1 or level > 3:
            return
        buffer = self.get_buffer()
        marker = f"/t{level}"
        close = f"t{level}/"
        self.engine.insert_markers(buffer, marker, close)
        self.engine.scan_around_cursor(buffer)

    def enlarge(self):
        """Increase the note window size by a percentage step.

        This is handled by the NoteWindow, not the editor itself.
        The shortcut controller passes this up.
        """
        # Get the toplevel window and call its enlarge method
        toplevel = self.get_root()
        if toplevel and hasattr(toplevel, "enlarge_note"):
            toplevel.enlarge_note()

    # --- Content extraction ---

    def get_markup_content(self) -> str:
        """Get full buffer content including hidden markers (for saving)."""
        return self.engine.get_markup_content(self.get_buffer())

    def get_visible_first_line(self) -> str:
        """Get the first visible line (for the manager list title)."""
        return self.engine.get_visible_first_line(self.get_buffer())

    def set_markup_content(self, text: str):
        """Load markup text into the editor and apply formatting.

        Args:
            text: Raw markup content (e.g., from JSON).
        """
        buffer = self.get_buffer()
        # Block changed signal during initial load to avoid
        # triggering save callbacks
        buffer.handler_block_by_func(self._on_buffer_changed)
        buffer.set_text(text)
        buffer.handler_unblock_by_func(self._on_buffer_changed)

        # Full scan to apply all formatting
        self.engine.scan_full(buffer)
