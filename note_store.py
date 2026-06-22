"""NoteStore — JSON file I/O for sticky notes.

Each note is stored as a single .json file in the notes/ directory.
The directory is created automatically if it doesn't exist.
"""

import json
import os
from datetime import datetime
from typing import List, Optional

from note_model import NoteModel


class NoteStore:
    """Manages CRUD operations for notes stored as JSON files."""

    def __init__(self, notes_dir: Optional[str] = None):
        """Initialize the store.

        Args:
            notes_dir: Path to the notes directory. Defaults to 'notes/'
                       relative to the project root.
        """
        if notes_dir is None:
            # Default to notes/ in the same directory as this file's parent
            notes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes")
        self.notes_dir = notes_dir
        os.makedirs(self.notes_dir, exist_ok=True)

    def _file_path(self, note_id: str) -> str:
        """Get the full file path for a note ID."""
        return os.path.join(self.notes_dir, f"{note_id}.json")

    def create(self, content: str = "", color: str = "yellow") -> NoteModel:
        """Create a new note with default values and save it immediately.

        Args:
            content: Initial text content.
            color: One of the five pastel colors.

        Returns:
            The newly created NoteModel.
        """
        note = NoteModel(content=content, color=color)
        self.save(note)
        return note

    def save(self, note: NoteModel) -> None:
        """Save a note to its JSON file (instant auto-save).

        Args:
            note: The NoteModel to persist.
        """
        note.modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = self._file_path(note.id)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(note.to_dict(), f, indent=2, ensure_ascii=False)

    def load_all(self) -> List[NoteModel]:
        """Load all notes from the notes directory.

        Returns:
            List of NoteModel objects, sorted by creation date (newest first).
        """
        notes = []
        if not os.path.isdir(self.notes_dir):
            return notes

        for filename in sorted(os.listdir(self.notes_dir), reverse=True):
            if not filename.endswith(".json"):
                continue
            file_path = os.path.join(self.notes_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                notes.append(NoteModel.from_dict(data))
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Warning: skipping corrupted note file {filename}: {e}")

        return notes

    def delete(self, note_id: str) -> bool:
        """Permanently delete a note's JSON file.

        Args:
            note_id: The ID of the note to delete.

        Returns:
            True if the file was deleted, False if it didn't exist.
        """
        file_path = self._file_path(note_id)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    def get(self, note_id: str) -> Optional[NoteModel]:
        """Load a single note by ID.

        Args:
            note_id: The note ID to look up.

        Returns:
            NoteModel if found, None otherwise.
        """
        file_path = self._file_path(note_id)
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return NoteModel.from_dict(data)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Warning: corrupted note file {note_id}.json: {e}")
            return None
