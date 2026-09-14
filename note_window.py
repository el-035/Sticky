"""NoteWindow — a floating sticky-note window.

Each note is an independent Gtk.Window with:
- A HeaderBar toolbar (bold, italic, title dropdown, color picker, close)
- A WysiwygEditor for text editing with real-time formatting
- Pastel background color (5 options, switchable via CSS classes)
- Ctrl+drag corner resize, Ctrl+Plus enlarge
- Instant auto-save on every keystroke
- Default post-it square size, cascade positioning
"""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("GLib", "2.0")

from gi.repository import Gtk, Gdk, GLib  # noqa: E402

from note_model import NoteModel  # noqa: E402
from wysiwyg_editor import WysiwygEditor  # noqa: E402
from css_styles import NOTE_CSS, PASTEL_COLORS, DEFAULT_COLOR  # noqa: E402


# Default note window size (post-it square)
DEFAULT_WIDTH = 320
DEFAULT_HEIGHT = 320

# Cascade offset for new windows
_cascade_offset = 0
CASCADE_STEP = 30
CASCADE_MAX = 300  # Reset after this many pixels


class NoteWindow(Gtk.Window):
    """A floating sticky-note window."""

    def __init__(self, app: Gtk.Application, note: NoteModel):
        super().__init__(
            application=app,
            title="Sticky Note",
            default_width=DEFAULT_WIDTH,
            default_height=DEFAULT_HEIGHT,
        )

        self.app = app
        self.note_model = note

        # Apply note CSS
        self.add_css_class("note-window")
        self._apply_css()
        self._set_color_class(note.color)

        # Build UI
        self._build_ui()
        self._set_color_button_color(note.color)

        # Load content into editor
        self.editor.set_markup_content(note.content)

        # Connect auto-save
        self.editor.on_content_changed_callback = self._auto_save

        # Setup resize via Ctrl+drag
        self._setup_resize()

        # Setup enlarge shortcut (Ctrl+Plus handled by editor, passed up)
        self._setup_enlarge_shortcut()

        # Setup local keyboard shortcuts for the note window
        self._setup_note_shortcuts()

        # Cascade position
        self._cascade_position()

        # Close handler
        self.connect("close-request", self._on_close_request)

    def _apply_css(self):
        """Load the note CSS provider."""
        provider = Gtk.CssProvider()
        provider.load_from_data(NOTE_CSS.encode("utf-8"))
        display = self.get_display()
        Gtk.StyleContext.add_provider_for_display(
            display, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _set_color_class(self, color: str):
        """Apply the CSS class for the given note color.

        Removes all existing color classes first, then adds the new one.
        """
        for color_info in PASTEL_COLORS.values():
            self.remove_css_class(color_info["css_class"])
        color_info = PASTEL_COLORS.get(color, PASTEL_COLORS[DEFAULT_COLOR])
        self.add_css_class(color_info["css_class"])

    def _set_color_button_color(self, color: str):
        """Show the selected note color as a swatch in the toolbar."""
        if not hasattr(self, "color_button"):
            return
        for color_name in PASTEL_COLORS:
            self.color_button.remove_css_class(f"color-{color_name}")
        selected = color if color in PASTEL_COLORS else DEFAULT_COLOR
        self.color_button.add_css_class(f"color-{selected}")
        color_info = PASTEL_COLORS[selected]
        self.color_button_label.set_markup(
            f'<span foreground="{color_info["hex"]}">●</span>'
        )

    def _build_ui(self):
        """Construct the note window layout."""
        # Main vertical box (toolbar + editor)
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        # --- Toolbar (simple box instead of HeaderBar) ---
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        toolbar.add_css_class("toolbar-box")
        toolbar.set_margin_start(6)
        toolbar.set_margin_end(6)
        toolbar.set_margin_top(4)
        toolbar.set_margin_bottom(4)
        toolbar.set_homogeneous(True)

        # Bold button
        bold_btn = Gtk.Button(label="B")
        bold_btn.set_tooltip_text("Bold (Ctrl+B)")
        bold_btn.connect("clicked", lambda b: self.editor.toggle_bold())
        toolbar.append(bold_btn)

        # Italic button
        italic_btn = Gtk.Button(label="I")
        italic_btn.set_tooltip_text("Italic (Ctrl+I)")
        italic_btn.connect("clicked", lambda b: self.editor.toggle_italic())
        toolbar.append(italic_btn)

        # Title dropdown (t1-t3)
        title_btn = Gtk.MenuButton()
        title_btn.add_css_class("title-button")
        title_btn.set_tooltip_text("Title levels (Ctrl+1 to Ctrl+3)")
        title_btn.set_label("T")
        title_popover = Gtk.Popover()
        title_popover.add_css_class("title-dropdown")
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        title_box.set_margin_start(6)
        title_box.set_margin_end(6)
        title_box.set_margin_top(6)
        title_box.set_margin_bottom(6)
        title_sizes = {1: 15000, 2: 12500, 3: 11000}
        for level in range(1, 4):
            btn = Gtk.Button()
            btn.add_css_class("title-option")
            title_label = Gtk.Label()
            title_label.set_markup(
                f'<span font_weight="bold" size="{title_sizes[level]}">Title</span>'
            )
            btn.set_child(title_label)
            btn.set_tooltip_text(f"Title level {level}")
            lvl = level
            btn.connect("clicked", lambda b, n=lvl: self._on_title_selected(n, title_popover))
            title_box.append(btn)
        title_popover.set_child(title_box)
        title_btn.set_popover(title_popover)
        toolbar.append(title_btn)

        # Color picker dropdown
        color_btn = Gtk.MenuButton()
        color_btn.add_css_class("color-button")
        self.color_button = color_btn
        self.color_button_label = Gtk.Label()
        color_btn.set_child(self.color_button_label)
        color_btn.set_tooltip_text("Note color")
        color_btn.add_css_class("color-dropdown")
        color_popover = Gtk.Popover()
        color_popover.add_css_class("color-dropdown")
        color_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        color_box.set_margin_start(6)
        color_box.set_margin_end(6)
        color_box.set_margin_top(6)
        color_box.set_margin_bottom(6)
        for color_name, color_info in PASTEL_COLORS.items():
            btn = Gtk.Button()
            swatch = Gtk.Label()
            swatch.set_markup(f'<span foreground="{color_info["hex"]}">●</span>')
            btn.set_child(swatch)
            btn.add_css_class("color-option")
            btn.add_css_class(f"color-{color_name}")
            btn.set_tooltip_text(f"Set note color to {color_info['name']}")
            cname = color_name
            btn.connect("clicked", lambda b, c=cname: self._on_color_selected(c, color_popover))
            color_box.append(btn)
        color_popover.set_child(color_box)
        color_btn.set_popover(color_popover)
        toolbar.append(color_btn)

        main_box.append(toolbar)

        # --- Title entry (separate, larger font) ---
        self.title_entry = Gtk.Entry()
        self.title_entry.set_placeholder_text("Title")
        self.title_entry.add_css_class("note-title-entry")
        self.title_entry.set_margin_start(8)
        self.title_entry.set_margin_end(8)
        self.title_entry.set_margin_top(6)
        self.title_entry.set_margin_bottom(2)
        self.title_entry.set_text(self.note_model.title)
        self.title_entry.connect("changed", self._on_title_changed)
        title_key_controller = Gtk.EventControllerKey.new()
        title_key_controller.connect("key-pressed", self._on_title_key_pressed)
        self.title_entry.add_controller(title_key_controller)
        main_box.append(self.title_entry)

        # --- Editor in ScrolledWindow ---
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.editor = WysiwygEditor()
        scrolled.set_child(self.editor)

        main_box.append(scrolled)
        self.set_child(main_box)

    def _setup_resize(self):
        """Setup Ctrl+drag resize from any corner.

        Uses a Gtk.GestureDrag that checks for Ctrl modifier.
        When Ctrl is held and the user drags near a corner, the window resizes.
        """
        drag = Gtk.GestureDrag()
        drag.connect("drag-begin", self._on_drag_begin)
        drag.connect("drag-update", self._on_drag_update)
        self.add_controller(drag)

    def _on_drag_begin(self, gesture, start_x, start_y):
        """Check if Ctrl is held at drag start."""
        event = gesture.get_last_event(None)
        if event is None:
            gesture.set_state(Gtk.EventSequenceState.DENIED)
            return

        # Check for Ctrl modifier
        state = event.get_modifier_state()
        if not (state & Gdk.ModifierType.CONTROL_MASK):
            gesture.set_state(Gtk.EventSequenceState.DENIED)
            return

        # Store initial window size
        self._drag_start_width = self.get_default_size()[0]
        self._drag_start_height = self.get_default_size()[1]
        gesture.set_state(Gtk.EventSequenceState.CLAIMED)

    def _on_drag_update(self, gesture, offset_x, offset_y):
        """Resize the window based on drag offset."""
        new_width = max(150, self._drag_start_width + int(offset_x))
        new_height = max(150, self._drag_start_height + int(offset_y))
        self.set_default_size(new_width, new_height)

    def _setup_enlarge_shortcut(self):
        """Ctrl+Plus enlarges the note by a percentage step."""
        # This is handled by the editor's shortcut controller,
        # which calls enlarge_note() on the toplevel window.
        pass

    def _setup_note_shortcuts(self):
        """Register note-window keyboard shortcuts.

        Ctrl+W closes the current note window.
        Ctrl+Alt+N creates a new note.
        """
        ctrl = Gtk.ShortcutController()
        ctrl.set_scope(Gtk.ShortcutScope.LOCAL)

        trigger = Gtk.ShortcutTrigger.parse_string("<Control>w")
        action = Gtk.CallbackAction.new(lambda w, e: self.close_note())
        ctrl.add_shortcut(Gtk.Shortcut.new(trigger=trigger, action=action))

        trigger = Gtk.ShortcutTrigger.parse_string("<Control><Alt>n")
        action = Gtk.CallbackAction.new(
            lambda w, e: self.app.activate_action("new-note", None)
        )
        ctrl.add_shortcut(Gtk.Shortcut.new(trigger=trigger, action=action))

        self.add_controller(ctrl)

    def enlarge_note(self):
        """Increase the note size by ~15%."""
        current_w, current_h = self.get_default_size()
        new_w = int(current_w * 1.15)
        new_h = int(current_h * 1.15)
        self.set_default_size(new_w, new_h)

    def _cascade_position(self):
        """Offset the window position slightly so new notes don't stack exactly."""
        global _cascade_offset
        # We can't get monitor geometry easily in GTK4 for cascade,
        # so just apply a simple offset from top-left
        # The window manager may override this anyway
        _cascade_offset = (_cascade_offset + CASCADE_STEP) % CASCADE_MAX

    def _on_title_selected(self, level: int, popover: Gtk.Popover):
        """Handle title level selection from dropdown."""
        popover.popdown()
        self.editor.apply_title(level)

    def _on_color_selected(self, color: str, popover: Gtk.Popover):
        """Handle color selection from dropdown."""
        popover.popdown()
        self.note_model.color = color
        self._set_color_class(color)
        self._set_color_button_color(color)
        self._auto_save()
        if self.app.manager_window is not None:
            self.app.manager_window.refresh_note_in_list(self.note_model)

    def _auto_save(self):
        """Save the note content to disk immediately."""
        self.note_model.content = self.editor.get_markup_content()
        self.app.note_store.save(self.note_model)

    def _on_title_key_pressed(self, controller, keyval, keycode, state):
        """Move focus from the title field to the note body on Tab."""
        if keyval == Gdk.KEY_Tab:
            self.editor.grab_focus()
            return True
        return False

    def _on_title_changed(self, entry):
        """Update the note title on every keystroke and save."""
        self.note_model.title = entry.get_text()
        self._auto_save()

        # If the manager list is visible, refresh this note's display title.
        if self.app.manager_window is not None:
            self.app.manager_window.refresh_note_in_list(self.note_model)

    def _on_close_btn_clicked(self, button):
        """Handle click on the X close button in the toolbar."""
        print(f"  [DEBUG] Close button clicked for note {self.note_model.id}")
        self.app.on_note_window_closed(self.note_model.id)
        # Defer destroy to avoid issues with destroying widget
        # while it's still processing the button event
        GLib.idle_add(self._deferred_destroy)

    def _deferred_destroy(self):
        """Destroy the window from an idle callback (safe context)."""
        print(f"  [DEBUG] deferred destroy for note {self.note_model.id}")
        self.destroy()
        return False  # Don't repeat

    def _on_close_request(self, window):
        """Handle the window manager close-request (Alt+F4, etc.).

        Closes the note window but the note remains in the list.
        """
        print(f"  [DEBUG] close-request for note {self.note_model.id}")
        self.app.on_note_window_closed(self.note_model.id)
        # Defer destroy to avoid issues
        GLib.idle_add(self._deferred_destroy)
        return True  # We handle the destroy ourselves

    def close_note(self):
        """Programmatic close — triggers cleanup and destroy."""
        self._on_close_btn_clicked(None)
