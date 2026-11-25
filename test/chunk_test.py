import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import split_into_chunks_word_boundary


def test_leading_space():
    text = " hello world "
    chunks = split_into_chunks_word_boundary(text, 6)
    assert "".join(chunks) == text
    assert all(len(chunk) <= 6 for chunk in chunks)

def test_multi_space():
    text = " hello  world "
    chunks = split_into_chunks_word_boundary(text, 6)
    assert "".join(chunks) == text
    assert all(len(chunk) <= 6 for chunk in chunks)

def test_single_word():
    text = "ABCDEFGHIJ"
    chunks = split_into_chunks_word_boundary(text, 4)
    assert "".join(chunks) == text
    assert all(len(chunk) <= 4 for chunk in chunks)

def test_empty_text():
    text = ""
    chunks = split_into_chunks_word_boundary(text, 6)
    assert "".join(chunks) == text
    assert all(len(chunk) <= 6 for chunk in chunks)

def test_multi_word():
    text = "abcdefgh ijklmnop"
    chunks = split_into_chunks_word_boundary(text, 5)
    assert "".join(chunks) == text
    assert all(len(chunk) <= 5 for chunk in chunks)