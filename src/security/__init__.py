"""Validações de segurança e caminhos."""

from src.security.validation import (
    MSG_FILE_NOT_FOUND,
    MSG_INTERNAL,
    MSG_INVALID_TS,
    MSG_MISSING_API_KEY,
    MSG_NO_INTERFACE,
    MSG_WRITE_FAIL,
    PathOutsideProjectError,
    ValidationError,
    assert_within_project_root,
    validate_file_size,
    validate_input_path,
)

__all__ = [
    "MSG_FILE_NOT_FOUND",
    "MSG_INTERNAL",
    "MSG_INVALID_TS",
    "MSG_MISSING_API_KEY",
    "MSG_NO_INTERFACE",
    "MSG_WRITE_FAIL",
    "PathOutsideProjectError",
    "ValidationError",
    "assert_within_project_root",
    "validate_file_size",
    "validate_input_path",
]
