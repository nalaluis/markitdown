"""MarkItDown - A utility for converting various file formats to Markdown.

This package provides tools to convert documents, spreadsheets, presentations,
and other file formats into clean, readable Markdown text.

Note: Forked from microsoft/markitdown for personal use and experimentation.

Personal additions/changes:
- Pinned version to track divergence from upstream
- Re-exported UnsupportedFormatException for easier error handling in scripts
"""

from markitdown._markitdown import MarkItDown, DocumentConverter, ConversionResult

__version__ = "0.1.0-personal"
__author__ = "MarkItDown Contributors"
__license__ = "MIT"

# Expose StreamInfo if available (added in newer versions of the upstream project)
try:
    from markitdown._markitdown import StreamInfo
    __all__ = [
        "MarkItDown",
        "DocumentConverter",
        "ConversionResult",
        "StreamInfo",
    ]
except ImportError:
    __all__ = [
        "MarkItDown",
        "DocumentConverter",
        "ConversionResult",
    ]

# Re-export UnsupportedFormatException so callers don't need to dig into internals
try:
    from markitdown._markitdown import UnsupportedFormatException
    __all__.append("UnsupportedFormatException")
except ImportError:
    pass
