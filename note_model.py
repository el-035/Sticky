"""NoteModel — pure data class for a single sticky note."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class NoteModel:
    """Represents a single sticky note with all its metadata."""

    id: str = ""
    title: str = ""
    content: str = ""
    color: str = "yellow"
    created: str = ""
    modified: str = ""

    def __post_init__(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not self.created:
            self.created = now
        if not self.modified:
            self.modified = now
        if not self.id:
            self.id = datetime.now().strftime("%Y%m%d-%H%M%S")

    def to_dict(self) -> dict:
        """Serialize to a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "color": self.color,
            "created": self.created,
            "modified": self.modified,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "NoteModel":
        """Deserialize from a dictionary (e.g., loaded from JSON)."""
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            content=data.get("content", ""),
            color=data.get("color", "yellow"),
            created=data.get("created", ""),
            modified=data.get("modified", ""),
        )

    @property
    def first_line(self) -> str:
        """Return the first non-empty line of content, or empty string."""
        for line in self.content.splitlines():
            stripped = line.strip()
            if stripped:
                return stripped
        return ""

    @property
    def visible_first_line(self) -> str:
        """Return the first line with formatting markers stripped out.

        Removes /b, b/, /i, i/, /t1-t3, t1/-t3/, and bullet '- ' prefixes.
        """
        import re

        text = self.first_line
        if not text:
            return ""

        # Remove formatting markers: /b, b/, /i, i/, /t1-t3, t1/-t3/
        text = re.sub(r'/([bit][1-4]?)', '', text)
        text = re.sub(r'([bit][1-4]?)/', '', text)

        # Remove bullet prefix
        text = re.sub(r'^- ', '', text)

        # Collapse multiple spaces left by removed markers
        text = re.sub(r' +', ' ', text)

        return text.strip()

    @property
    def display_title(self) -> str:
        """Return a human-readable title.

        Priority:
        1. Explicit title field
        2. Visible first line of content
        3. Creation date
        """
        title = self.title.strip()
        if title:
            return title

        visible = self.visible_first_line
        if visible:
            return visible

        return self.created
