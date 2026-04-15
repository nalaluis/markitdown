"""Core MarkItDown conversion engine.

This module provides the main MarkItDown class and supporting utilities
for converting various file formats to Markdown.
"""

from __future__ import annotations

import os
import re
import mimetypes
from pathlib import Path
from typing import Optional, Union
from dataclasses import dataclass, field


@dataclass
class DocumentConverterResult:
    """Result of a document conversion operation."""

    title: Optional[str] = None
    text_content: str = ""
    metadata: dict = field(default_factory=dict)

    def __str__(self) -> str:
        return self.text_content


class DocumentConverter:
    """Base class for all document converters."""

    def convert(
        self,
        local_path: str,
        file_extension: Optional[str] = None,
        **kwargs,
    ) -> Optional[DocumentConverterResult]:
        """Convert a document at the given path to Markdown.

        Args:
            local_path: Path to the file to convert.
            file_extension: Optional file extension hint.
            **kwargs: Additional converter-specific arguments.

        Returns:
            A DocumentConverterResult if conversion was successful, else None.
        """
        raise NotImplementedError("Subclasses must implement convert()")


class MarkItDown:
    """Main class for converting documents to Markdown format.

    Supports a variety of file formats through a pluggable converter system.
    Converters are tried in registration order; the first successful result
    is returned.

    Example::

        md = MarkItDown()
        result = md.convert("document.pdf")
        print(result.text_content)
    """

    def __init__(self) -> None:
        self._converters: list[DocumentConverter] = []
        self._register_default_converters()

    def _register_default_converters(self) -> None:
        """Register the built-in converters in priority order."""
        # Import here to avoid circular imports and allow optional dependencies
        from markitdown.converters import (
            PlainTextConverter,
            HtmlConverter,
        )

        self.register_converter(self.register_converter(HtmlConverter())

    def register_converter(self, converter: DocumentConverter) -> None:
        """Register a new converter.

        Converters registered later priority than those registered
        earlier unless prepend=True is used.

        Args:
            converter: A DocumentConverter instance to register.
        """
        self._converters.append(converter)

    def convert(
        self,
        source: Union[str, Path],
        **kwargs,
    ) -> DocumentConverterResult:
        """Convert a file or URL to Markdown.

        Args:
            source: A file path or URL string to convert.
            **kwargs: Additional arguments forwarded to converters.

        Returns:
            A DocumentConverterResult containing the Markdown text.

        Raises:
            FileNotFoundError: If the source file does not exist.
            ValueError: If no converter could handle the source.
        """
        source = str(source)

        # Resolve local file path
        if not source.startswith(("http://", "https://")):
            path = Path(source).expanduser().resolve()
            if not path.exists():
                raise FileNotFoundError(f"File not found: {source}")
            return self._convert_local(str(path), **kwargs)

        raise ValueError(f"URL conversion is not yet supported: {source}")

    def _convert_local(
        self,
        local_path: str,
        **kwargs,
    ) -> DocumentConverterResult:
        """Attempt conversion using registered converters."""
        ext = os.path.splitext(local_path)[-1].lower()
        mime_type, _ = mimetypes.guess_type(local_path)

        for converter in self._converters:
            result = converter.convert(
                local_path,
                file_extension=ext,
                mime_type=mime_type,
                **kwargs,
            )
            if result is not None:
                return result

        raise ValueError(
            f"No converter found for file: {local_path} (extension={ext}, mime={mime_type})"
        )
