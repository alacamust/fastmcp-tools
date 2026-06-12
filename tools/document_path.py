import os
from pydantic import Field
from tools.document import binary_document_to_markdown


def document_path_to_markdown(
    path: str = Field(description="Absolute or relative path to a PDF or DOCX file"),
) -> str:
    """Convert a PDF or DOCX file at the given path to markdown text.

    Reads the file at the specified path and converts its contents to
    markdown-formatted text. The file type is inferred from the file extension.

    When to use:
    - When you have a local file path and want to extract its text as markdown
    - When processing PDF or DOCX documents stored on disk

    When NOT to use:
    - When you already have the file contents in memory as bytes — use binary_document_to_markdown instead
    - For file types other than PDF and DOCX

    Examples:
    >>> document_path_to_markdown("/tmp/report.pdf")
    "# Report Title\\n\\nSome content..."
    >>> document_path_to_markdown("docs/spec.docx")
    "# Spec\\n\\n- Item one..."
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No file found at path: {path}")

    _, ext = os.path.splitext(path)
    file_type = ext.lstrip(".").lower()

    if file_type not in ("pdf", "docx"):
        raise ValueError(f"Unsupported file type: '{ext}'. Only PDF and DOCX are supported.")

    with open(path, "rb") as f:
        data = f.read()

    return binary_document_to_markdown(data, file_type)
