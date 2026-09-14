"""FormattingEngine — detects markup markers and applies Gtk.TextTags.

Handles the custom formatting syntax:
  /b ... b/  → bold
  /i ... i/  → italic
  /t1 ... t1/ through /t3 ... t3/  → titles (scaled font sizes)
  - at line start → bullet list (the "- " prefix is hidden)

Uses invisible TextTags to hide markers while keeping them in the buffer.
Runs on every keystroke, scoped to cursor-adjacent lines for performance.
"""

import re
from typing import Optional, Tuple

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Pango", "1.0")

from gi.repository import Gtk, Pango  # noqa: E402


class FormattingEngine:
    """Applies and manages formatting tags on a Gtk.TextBuffer.

    Stateless — all state is in the TextBuffer's tags and content.
    """

    # Marker patterns: (open_marker, close_marker, tag_name)
    MARKERS = [
        ("/b", "b/", "b"),
        ("/i", "i/", "i"),
        ("/t1", "t1/", "t1"),
        ("/t2", "t2/", "t2"),
        ("/t3", "t3/", "t3"),
    ]

    # Tag names that this engine manages
    STYLE_TAGS = {"b", "i", "t1", "t2", "t3"}
    HIDDEN_TAGS = {"marker", "bullet"}
    ALL_TAGS = STYLE_TAGS | HIDDEN_TAGS

    def __init__(self):
        """Initialize the engine. Call setup_tags() on each TextBuffer."""
        pass

    def setup_tags(self, buffer: Gtk.TextBuffer):
        """Create all formatting tags on the given buffer.

        Must be called once per buffer before any formatting is applied.
        """
        tag_table = buffer.get_tag_table()

        # Bold tag
        if tag_table.lookup("b") is None:
            tag = buffer.create_tag("b", weight=Pango.Weight.BOLD)

        # Italic tag
        if tag_table.lookup("i") is None:
            buffer.create_tag("i", style=Pango.Style.ITALIC)

        # Title tags — scaled font sizes with bold
        title_specs = {
            "t1": (1.5, Pango.Weight.BOLD),
            "t2": (1.25, Pango.Weight.BOLD),
            "t3": (1.1, Pango.Weight.BOLD),
        }
        for tag_name, (scale, weight) in title_specs.items():
            if tag_table.lookup(tag_name) is None:
                buffer.create_tag(tag_name, scale=scale, weight=weight)

        # Marker tag — makes formatting markers invisible
        if tag_table.lookup("marker") is None:
            buffer.create_tag("marker", invisible=True)

        # Bullet tag — hides the "- " prefix on list lines
        if tag_table.lookup("bullet") is None:
            buffer.create_tag("bullet", invisible=True)

    def scan_and_apply(
        self, buffer: Gtk.TextBuffer, start_iter: Gtk.TextIter, end_iter: Gtk.TextIter
    ):
        """Scan a region of the buffer and apply formatting tags.

        This is the main entry point. Called on every text change.
        Scans for marker pairs and bullet patterns, then applies
        the appropriate TextTags.

        Args:
            buffer: The Gtk.TextBuffer to format.
            start_iter: Start of the region to scan.
            end_iter: End of the region to scan.
        """
        # Get the full text of the region (including hidden characters)
        text = buffer.get_text(start_iter, end_iter, True)

        # Remove all formatting tags in this region (reset state)
        for tag_name in self.ALL_TAGS:
            buffer.remove_tag_by_name(tag_name, start_iter, end_iter)

        # Apply markers. Bullet '- ' markers stay visible (Markdown-style)
        # so the user sees what they typed, but Enter/Backspace still treat
        # bullet lines specially.
        self._apply_markers(buffer, text, start_iter)

    def scan_around_cursor(self, buffer: Gtk.TextBuffer):
        """Scan the region around the cursor for performance.

        Only scans a few lines around the current insert position,
        since formatting changes are local to where the user is typing.

        Args:
            buffer: The Gtk.TextBuffer.
        """
        insert_mark = buffer.get_insert()
        cursor_iter = buffer.get_iter_at_mark(insert_mark)

        # Expand to cover a few lines around cursor
        start_iter = cursor_iter.copy()
        end_iter = cursor_iter.copy()

        # Go back 3 lines (or to buffer start)
        for _ in range(3):
            if not start_iter.backward_line():
                break
        # If we moved back, go to line start
        if not start_iter.starts_line():
            start_iter.set_line_offset(0)

        # Go forward 3 lines (or to buffer end)
        for _ in range(3):
            if not end_iter.forward_line():
                break
        if not end_iter.ends_line():
            end_iter.forward_to_line_end()

        self.scan_and_apply(buffer, start_iter, end_iter)

    def scan_full(self, buffer: Gtk.TextBuffer):
        """Scan the entire buffer. Used on initial note load."""
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        self.scan_and_apply(buffer, start, end)

    def _apply_markers(
        self, buffer: Gtk.TextBuffer, text: str, region_start: Gtk.TextIter
    ):
        """Find marker pairs in text and apply style + marker tags.

        For each complete pair like /b ... b/, applies:
        - The style tag (e.g., "b") to the content between markers
        - The "marker" tag (invisible) to the markers themselves

        For incomplete pairs (opening marker without closing), applies:
        - The style tag from the opening marker to end of region
        - The "marker" tag to the opening marker only
        """
        for open_marker, close_marker, tag_name in self.MARKERS:
            # Find complete pairs: open_marker ... close_marker
            # Escape markers for regex (they contain / which is not special)
            open_re = re.escape(open_marker)
            close_re = re.escape(close_marker)

            # Pattern: non-greedy match of content between markers
            pattern = f"{open_re}(.*?){close_re}"
            for match in re.finditer(pattern, text, re.DOTALL):
                content_start = match.start(1)
                content_end = match.end(1)
                marker_open_start = match.start(0)
                marker_open_end = match.start(1)  # end of open marker
                marker_close_start = match.end(1)  # start of close marker
                marker_close_end = match.end(0)

                # Apply style tag to content
                self._apply_tag_at_offset(
                    buffer, region_start, tag_name, content_start, content_end
                )
                # Apply marker tag to open marker
                self._apply_tag_at_offset(
                    buffer, region_start, "marker", marker_open_start, marker_open_end
                )
                # Apply marker tag to close marker
                self._apply_tag_at_offset(
                    buffer, region_start, "marker", marker_close_start, marker_close_end
                )

            # Find incomplete open markers (no matching close in this region)
            open_pattern = f"{open_re}(?!.*?{close_re})"
            for match in re.finditer(open_pattern, text, re.DOTALL):
                marker_start = match.start(0)
                marker_end = match.end(0)

                # Apply marker tag to the open marker
                self._apply_tag_at_offset(
                    buffer, region_start, "marker", marker_start, marker_end
                )
                # Apply style tag from marker end to end of text
                self._apply_tag_at_offset(
                    buffer, region_start, tag_name, marker_end, len(text)
                )

    def _apply_bullets(
        self, buffer: Gtk.TextBuffer, text: str, region_start: Gtk.TextIter
    ):
        """Find bullet patterns (- at line start) and hide the '- ' prefix.

        A bullet line is one that starts with '- ' (dash + space).
        The '- ' prefix gets the 'bullet' tag (invisible).
        """
        for match in re.finditer(r"^[ ]*- ", text, re.MULTILINE):
            bullet_start = match.start(0)
            bullet_end = match.end(0)  # covers "- "
            self._apply_tag_at_offset(
                buffer, region_start, "bullet", bullet_start, bullet_end
            )

    def _apply_tag_at_offset(
        self,
        buffer: Gtk.TextBuffer,
        region_start: Gtk.TextIter,
        tag_name: str,
        offset_start: int,
        offset_end: int,
    ):
        """Apply a tag to a character range given as offsets from region_start.

        Args:
            buffer: The TextBuffer.
            region_start: The start iter of the scanned region.
            tag_name: Name of the tag to apply.
            offset_start: Character offset from region_start for tag start.
            offset_end: Character offset from region_start for tag end.
        """
        if offset_start >= offset_end:
            return

        tag_start = region_start.copy()
        tag_start.forward_chars(offset_start)

        tag_end = region_start.copy()
        tag_end.forward_chars(offset_end)

        buffer.apply_tag_by_name(tag_name, tag_start, tag_end)

    def get_markup_content(self, buffer: Gtk.TextBuffer) -> str:
        """Get the full buffer content including hidden markers.

        This is what gets saved to JSON — raw markup preserved.
        """
        return buffer.get_text(
            buffer.get_start_iter(), buffer.get_end_iter(), True
        )

    def get_visible_content(self, buffer: Gtk.TextBuffer) -> str:
        """Get only visible text (markers and bullets hidden).

        Used for display in the manager list preview.
        """
        return buffer.get_text(
            buffer.get_start_iter(), buffer.get_end_iter(), False
        )

    def get_visible_first_line(self, buffer: Gtk.TextBuffer) -> str:
        """Get the first visible line of the buffer.

        Used for the note title in the manager list.
        """
        visible = self.get_visible_content(buffer)
        for line in visible.splitlines():
            stripped = line.strip()
            if stripped:
                return stripped
        return ""

    def insert_markers(
        self, buffer: Gtk.TextBuffer, open_marker: str, close_marker: str
    ):
        """Insert formatting markers around the current selection or cursor position.

        If text is selected, wraps the selection with markers.
        If no selection, inserts both markers at cursor (user types between them).

        Args:
            buffer: The TextBuffer.
            open_marker: e.g., '/b'
            close_marker: e.g., 'b/'
        """
        # Get selection bounds — returns () if no selection
        bounds = buffer.get_selection_bounds()
        if bounds:
            start_iter, end_iter = bounds
        else:
            start_iter, end_iter = None, None

        if start_iter is not None and end_iter is not None and start_iter.compare(end_iter) < 0:
            # Wrap selection with markers.
            # Use marks to preserve positions across buffer modifications.
            start_mark = buffer.create_mark(None, start_iter, True)
            end_mark = buffer.create_mark(None, end_iter, False)

            # Insert close marker at end, then open marker at start
            end_pos = buffer.get_iter_at_mark(end_mark)
            buffer.insert(end_pos, close_marker)

            start_pos = buffer.get_iter_at_mark(start_mark)
            buffer.insert(start_pos, open_marker)

            # Clean up marks
            buffer.delete_mark(start_mark)
            buffer.delete_mark(end_mark)
        else:
            # No selection — insert both markers at cursor,
            # then place cursor between them.
            cursor_mark = buffer.create_mark(None, buffer.get_iter_at_mark(buffer.get_insert()), True)

            # Insert close marker first (right gravity), then open marker
            cursor_pos = buffer.get_iter_at_mark(cursor_mark)
            buffer.insert(cursor_pos, close_marker)

            cursor_pos = buffer.get_iter_at_mark(cursor_mark)
            buffer.insert(cursor_pos, open_marker)

            # Place cursor between open and close markers
            cursor_pos = buffer.get_iter_at_mark(cursor_mark)
            buffer.place_cursor(cursor_pos)

            buffer.delete_mark(cursor_mark)

    def _line_text_at_cursor(self, buffer: Gtk.TextBuffer) -> str:
        """Return the raw text of the line containing the cursor."""
        cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())
        line_start = cursor_iter.copy()
        line_start.set_line_offset(0)

        line_end = cursor_iter.copy()
        if not line_end.ends_line():
            line_end.forward_to_line_end()

        return buffer.get_text(line_start, line_end, True)

    def is_bullet_line(self, buffer: Gtk.TextBuffer) -> bool:
        """Check if the current line (at cursor) is a bullet list line.

        Args:
            buffer: The TextBuffer.

        Returns:
            True if the line containing the cursor starts with '- '.
        """
        line_text = self._line_text_at_cursor(buffer)
        return bool(re.match(r"^[ ]*- ", line_text))

    def is_empty_bullet_line(self, buffer: Gtk.TextBuffer) -> bool:
        """Check if the current line is an empty bullet (just '- ').

        Args:
            buffer: The TextBuffer.

        Returns:
            True if the line is only the bullet prefix.
        """
        line_text = self._line_text_at_cursor(buffer)
        return line_text.strip() == "-"

    def insert_bullet_on_enter(self, buffer: Gtk.TextBuffer):
        """Insert a newline plus '- ' and leave the cursor after the '- '.

        Call this from the key-pressed handler when Enter is detected
        on a bullet line. The bullet prefix will be hidden by the next scan.

        Args:
            buffer: The TextBuffer.
        """
        cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())
        indent = self.bullet_indentation(buffer)
        # Insert a newline plus the same indentation and bullet prefix.
        buffer.insert(cursor_iter, f"\n{indent}- ")

    def bullet_indentation(self, buffer: Gtk.TextBuffer) -> str:
        """Return the spaces before the current line's bullet marker."""
        line_text = self._line_text_at_cursor(buffer)
        match = re.match(r"^( *)- ", line_text)
        return match.group(1) if match else ""

    def indent_bullet(self, buffer: Gtk.TextBuffer, spaces: int = 4) -> bool:
        """Indent the current bullet line by the requested number of spaces."""
        if not self.is_bullet_line(buffer):
            return False
        cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())
        line_start = cursor_iter.copy()
        line_start.set_line_offset(0)
        buffer.insert(line_start, " " * spaces)
        return True

    def outdent_empty_bullet(self, buffer: Gtk.TextBuffer, spaces: int = 4) -> bool:
        """Remove one indentation level from an empty nested bullet."""
        if not self.is_empty_bullet_line(buffer):
            return False
        indent = self.bullet_indentation(buffer)
        if len(indent) < spaces:
            return False

        cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())
        line_start = cursor_iter.copy()
        line_start.set_line_offset(0)
        line_end = line_start.copy()
        line_end.forward_chars(spaces)
        buffer.delete(line_start, line_end)
        return True

    def delete_empty_bullet(self, buffer: Gtk.TextBuffer) -> bool:
        """If the current line is an empty bullet, delete it entirely.

        Call this from the key-pressed handler when BackSpace is detected.

        Args:
            buffer: The TextBuffer.

        Returns:
            True if an empty bullet was deleted, False otherwise.
        """
        if not self.is_empty_bullet_line(buffer):
            return False

        cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())
        line_start = cursor_iter.copy()
        line_start.set_line_offset(0)

        line_end = cursor_iter.copy()
        if not line_end.ends_line():
            line_end.forward_to_line_end()

        # Delete the entire line including the newline
        # Extend line_end past the newline character
        if line_end.forward_char():
            pass  # Now line_end is at the start of the next line

        buffer.delete(line_start, line_end)
        return True
