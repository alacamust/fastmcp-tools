import os
import pytest
from tools.document_path import document_path_to_markdown


FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")
DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")


class TestDocumentPathToMarkdown:
    def test_pdf_returns_markdown_string(self):
        result = document_path_to_markdown(PDF_FIXTURE)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_docx_returns_markdown_string(self):
        result = document_path_to_markdown(DOCX_FIXTURE)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_pdf_contains_markdown_formatting(self):
        result = document_path_to_markdown(PDF_FIXTURE)
        assert "#" in result or "-" in result or "*" in result

    def test_docx_contains_markdown_formatting(self):
        result = document_path_to_markdown(DOCX_FIXTURE)
        assert "#" in result or "-" in result or "*" in result

    def test_uppercase_extension_is_accepted(self, tmp_path):
        upper = tmp_path / "doc.PDF"
        upper.write_bytes(open(PDF_FIXTURE, "rb").read())
        result = document_path_to_markdown(str(upper))
        assert len(result) > 0

    def test_mixed_case_extension_is_accepted(self, tmp_path):
        mixed = tmp_path / "doc.Docx"
        mixed.write_bytes(open(DOCX_FIXTURE, "rb").read())
        result = document_path_to_markdown(str(mixed))
        assert len(result) > 0

    def test_path_with_spaces(self, tmp_path):
        spaced = tmp_path / "my document.pdf"
        spaced.write_bytes(open(PDF_FIXTURE, "rb").read())
        result = document_path_to_markdown(str(spaced))
        assert len(result) > 0

    def test_relative_path(self):
        rel = os.path.relpath(PDF_FIXTURE)
        result = document_path_to_markdown(rel)
        assert len(result) > 0

    def test_missing_file_raises_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            document_path_to_markdown("/nonexistent/path/file.pdf")

    def test_unsupported_extension_raises_value_error(self, tmp_path):
        bad = tmp_path / "file.txt"
        bad.write_text("hello")
        with pytest.raises(ValueError, match="Unsupported file type"):
            document_path_to_markdown(str(bad))

    def test_no_extension_raises_value_error(self, tmp_path):
        no_ext = tmp_path / "file"
        no_ext.write_text("hello")
        with pytest.raises(ValueError, match="Unsupported file type"):
            document_path_to_markdown(str(no_ext))
