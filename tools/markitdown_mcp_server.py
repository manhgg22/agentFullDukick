"""
MarkItDown MCP server (stdio) for all Dukick Hermes agents.
Wraps Microsoft MarkItDown lib -> exposes `convert_to_markdown` tool.
Run: python markitdown_mcp_server.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from fastmcp import FastMCP
from markitdown import MarkItDown

mcp = FastMCP("markitdown")
_mdi = MarkItDown()


@mcp.tool()
def convert_to_markdown(source: str) -> str:
    """Convert a local file or URL to Markdown.

    Supports: PDF, DOCX, XLSX, PPTX, HTML, CSV, JSON, XML, images (OCR-ish via vision models),
    audio (transcribe), YouTube URLs, ZIP, and more. Uses Microsoft MarkItDown.

    Args:
        source: Absolute local file path OR http(s) URL.

    Returns:
        Markdown text of the converted document. Empty string if nothing extracted.
    """
    try:
        result = _mdi.convert(source)
        return result.text_content or ""
    except Exception as exc:  # surface error to agent, never crash server
        return f"[markitdown error] {type(exc).__name__}: {exc}"


@mcp.tool()
def list_markitdown_supported() -> str:
    """List file types MarkItDown can convert."""
    return (
        "MarkItDown supports: PDF, DOCX, DOC, XLSX, XLS, PPTX, PPT, HTML, HTM, "
        "CSV, TSV, JSON, XML, TXT, MD, Markdown, JPG/JPEG, PNG, GIF, BMP, TIFF, "
        "WAV, MP3, M4A (audio transcription), YouTube URLs, ZIP (extracts first doc), "
        "and Outlook MSG/EML. Pass an absolute path or URL to convert_to_markdown."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")