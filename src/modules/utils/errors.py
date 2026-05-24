"""
Application error types and formatting helpers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ApplicationError(Exception):
    """Base error carrying a user message plus technical context."""

    message: str
    code: str = "APP_ERROR"
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return self.message


class ValidationError(ApplicationError):
    """Raised for user-fixable validation failures."""


class FileOperationError(ApplicationError):
    """Raised when a file operation fails but the app can keep running."""


def readable_error(error: BaseException) -> str:
    """Return a concise error message suitable for UI details and logs."""
    if isinstance(error, ApplicationError):
        return error.message
    return str(error) or error.__class__.__name__


def file_error_message(action: str, file_name: str, error: BaseException) -> str:
    """Format a per-file operation failure with enough context for the user."""
    return f"{file_name}: {action} failed ({readable_error(error)})"
