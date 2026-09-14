"""ManagerWindow — the main note list view.

Compact post-it style manager list.
Shows all notes in a Gtk.ListView with first-line preview, color indicator,
and a delete button per row. Has a "+" button.
"""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gio", "2.0")
gi.require_version("GObject", "2.0")

from gi.repository import Gtk, Gio, GObject, GLib  # noqa: E402

from note_model import NoteModel  # noqa: E402
from css_styles import MANAGER_CSS, PASTEL_COLORS  # noqa: E402


class NoteRow(GObject.Object):
    """GObject wrapper for note data displayed in a ListView row.

    Gio.ListStore requires GObject-based items. This wraps the
    display-relevant fields of a NoteModel for the list view.
    """

    note_id = GObject.Property(type=str)
    display_title = GObject.Property(type=str)
    color = GObject.Property(type=str)
    created = GObject.Property(type=str)
    locked = GObject.Property(type=bool, default=False)

    def __init__(self, note: NoteModel):
        super().__init__()
        self.note_id = note.id
        self.display_title = note.display_title
        self.color = note.color
        self.created = note.created
        self.locked = note.locked
        self._title = note.title
        self._content = note.content

    @classmethod
    def from_note(cls, note: NoteModel) -> "NoteRow":
        return cls(note)


class ManagerWindow(Gtk.ApplicationWindow):
    """The main window showing all notes in a list."""

    def __init__(self, app: Gtk.Application):
        super().__init__(
            application=app,
            title="Sticky",
            default_width=420,
            default_height=560,
        )

        # Per-widget bound data storage. PyGObject on some systems does not
        # support GObject.set_data(), so we keep our own maps keyed by widget.
        self._widget_note_ids: dict[int, str] = {}

        # Apply post-it manager CSS
        self.add_css_class("manager")
        self._apply_css()

        # Data store for the list
        self.list_store = Gio.ListStore(item_type=NoteRow)

        # Build UI
        self._build_ui()

        # Load existing notes
        self._load_notes(app.note_store)

    def _apply_css(self):
        """Load the manager CSS provider."""
        provider = Gtk.CssProvider()
        provider.load_from_data(MANAGER_CSS.encode("utf-8"))
        display = self.get_display()
        Gtk.StyleContext.add_provider_for_display(
            display, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _build_ui(self):
        """Construct the window layout."""
        # Main vertical box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_child(vbox)

        # --- Scrolled list view ---
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.list_view = Gtk.ListView()
        self.list_view.set_model(Gtk.SingleSelection(model=self.list_store))
        self.list_view.add_css_class("listview")

        # Factory: how each row is built
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_list_item_setup)
        factory.connect("bind", self._on_list_item_bind)
        factory.connect("unbind", self._on_list_item_unbind)
        self.list_view.set_factory(factory)

        # Activate on click
        self.list_view.connect("activate", self._on_row_activated)

        scrolled.set_child(self.list_view)
        vbox.append(scrolled)

        # --- Bottom-right new-note button ---
        footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        footer.set_halign(Gtk.Align.END)
        footer.set_margin_end(12)
        footer.set_margin_top(8)
        footer.set_margin_bottom(12)
        add_button = Gtk.Button(label="+")
        add_button.add_css_class("add-button")
        add_button.set_tooltip_text("New note (Ctrl+Alt+N)")
        add_button.connect("clicked", self._on_add_clicked)
        footer.append(add_button)
        vbox.append(footer)

        # --- Close-request: destroy manager, let GTK quit when last window closes ---
        self.connect("close-request", self._on_close_request)

    def _on_list_item_setup(self, factory, list_item):
        """Create the row widget structure (called once per row template)."""
        row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row_box.set_margin_start(16)
        row_box.set_margin_end(16)
        row_box.set_margin_top(5)
        row_box.set_margin_bottom(5)

        # Whole-row click opens the note. The row_box gesture sees clicks on
        # empty space and on non-target children; the delete button consumes
        # its own clicks and is not opened.
        row_click = Gtk.GestureClick()
        row_click.connect("released", self._on_row_clicked, list_item)
        row_box.add_controller(row_click)

        # Color indicator dot (visual only)
        color_dot = Gtk.Label()
        color_dot.set_size_request(12, 12)
        color_dot.set_label("●")
        color_dot.add_css_class("color-dot")
        color_dot.set_can_target(False)
        row_box.append(color_dot)

        # Title label (visual only, let clicks pass through to the row)
        title_label = Gtk.Label()
        title_label.set_halign(Gtk.Align.START)
        title_label.set_hexpand(True)
        title_label.set_ellipsize(3)  # PANGO_ELLIPSIZE_END
        title_label.set_max_width_chars(40)
        title_label.add_css_class("title-label")
        title_label.set_can_target(False)
        row_box.append(title_label)

        # Lock button — toggles deletion protection without opening the note.
        lock_btn = Gtk.Button()
        lock_btn.add_css_class("lock-button")
        lock_btn.set_can_target(True)
        lock_btn.connect("clicked", self._on_lock_clicked, list_item)
        row_box.append(lock_btn)

        # Delete button — pass the list_item so we can read the current note on click
        delete_btn = Gtk.Button(label="✕")
        delete_btn.add_css_class("delete-button")
        delete_btn.set_tooltip_text("Delete note")
        delete_btn.set_can_target(True)
        delete_btn.connect("clicked", self._on_delete_clicked, list_item)
        row_box.append(delete_btn)

        list_item.set_child(row_box)

        # Disable row-level selection/focus so the row itself doesn't fight the
        # child widgets for events. We still get whole-row clicks via row_click.
        list_item.set_selectable(False)
        list_item.set_focusable(False)

    def _on_list_item_bind(self, factory, list_item):
        """Bind data from a NoteRow to the row widgets."""
        row_box = list_item.get_child()
        note_row = list_item.get_item()  # NoteRow

        color_dot = row_box.get_first_child()
        title_label = color_dot.get_next_sibling()
        lock_btn = title_label.get_next_sibling()

        note_id = note_row.note_id
        self._widget_note_ids[id(color_dot)] = note_id
        self._widget_note_ids[id(title_label)] = note_id

        # Update bound title from the underlying model when refreshing the list.
        self._widget_note_ids[id(title_label)] = note_row.note_id

        # Set title and dot color
        title_label.set_label(note_row.display_title)
        color_info = PASTEL_COLORS.get(note_row.color, PASTEL_COLORS["yellow"])
        color_dot.set_markup(
            f'<span foreground="{color_info["hex"]}">●</span>'
        )
        self._update_lock_button(lock_btn, note_row)

    def _on_list_item_unbind(self, factory, list_item):
        """Unbind data (clean up references)."""
        row_box = list_item.get_child()
        if row_box is None:
            return
        color_dot = row_box.get_first_child()
        title_label = color_dot.get_next_sibling()
        lock_btn = title_label.get_next_sibling()
        for child in (color_dot, title_label, lock_btn):
            if child:
                self._widget_note_ids.pop(id(child), None)

    def _get_note_id(self, widget):
        """Return the bound note_id for a widget, if any."""
        return self._widget_note_ids.get(id(widget))

    def _on_row_clicked(self, gesture, n_press, x, y, list_item):
        """Handle single-click anywhere on the row — open the note."""
        # Ignore double/triple presses; open on a single click.
        if n_press != 1:
            return

        item = list_item.get_item()
        if item is None:
            return

        note_id = item.note_id
        app = self.get_application()
        if app:
            app.on_note_activated(note_id)

    def _on_row_activated(self, list_view, position):
        """Handle double-click/Enter on a list row — open the note."""
        selected = self.list_view.get_model()
        item = selected.get_item(position)
        if item is None:
            return

        note_id = item.note_id
        app = self.get_application()
        app.on_note_activated(note_id)

    def _update_lock_button(self, button, note_row):
        """Reflect a note's lock state with a simple open/closed icon."""
        icon_name = "changes-prevent-symbolic" if note_row.locked else "changes-allow-symbolic"
        icon = Gtk.Image.new_from_icon_name(icon_name)
        icon.set_pixel_size(16)
        button.set_child(icon)
        if note_row.locked:
            button.set_tooltip_text("Unlock note")
            button.add_css_class("is-locked")
        else:
            button.set_tooltip_text("Lock note to prevent deletion")
            button.remove_css_class("is-locked")

    def _on_lock_clicked(self, button, list_item):
        """Toggle deletion protection for a note."""
        item = list_item.get_item()
        if item is None:
            return
        app = self.get_application()
        note = app.note_store.get(item.note_id) if app else None
        if note is None:
            return
        note.locked = not note.locked
        app.note_store.save(note)
        item.locked = note.locked
        self._update_lock_button(button, item)

    def _on_delete_clicked(self, button, list_item):
        """Handle click on a delete button — instant delete, no confirmation."""
        item = list_item.get_item()
        if item is None:
            return

        note_id = item.note_id
        if item.locked:
            return
        app = self.get_application()
        app.on_note_deleted(note_id)

        # Remove from list store
        self._remove_from_store(note_id)

    def _on_add_clicked(self, button):
        """Create a new note."""
        app = self.get_application()
        app.activate_action("new-note", None)

    def _on_close_request(self, window):
        """Destroy the manager window.

        The app quits automatically when the last window (manager or note)
        is closed, so we do not force-quit here.
        """
        self.destroy()
        return True

    def _load_notes(self, note_store):
        """Populate the list with all existing notes from the store."""
        notes = note_store.load_all()
        for note in notes:
            self.list_store.append(NoteRow.from_note(note))

    def add_note_to_list(self, note: NoteModel):
        """Add a newly created note to the top of the list."""
        self.list_store.insert(0, NoteRow.from_note(note))

    def _remove_from_store(self, note_id: str):
        """Remove a note row from the ListStore by its ID."""
        for i in range(self.list_store.get_n_items()):
            item = self.list_store.get_item(i)
            if item and item.note_id == note_id:
                self.list_store.remove(i)
                break

    def refresh_note_in_list(self, note: NoteModel):
        """Refresh an existing note row after note metadata changes.

        Gio.ListStore does not notify views about in-place item changes,
        so we replace the row when its title, color, or lock state changes.
        """
        note_id = note.id
        for i in range(self.list_store.get_n_items()):
            item = self.list_store.get_item(i)
            if item is None or item.note_id != note_id:
                continue

            if (
                item.display_title != note.display_title
                or item.color != note.color
                or item.locked != note.locked
            ):
                self.list_store.remove(i)
                self.list_store.insert(i, NoteRow.from_note(note))
            break
