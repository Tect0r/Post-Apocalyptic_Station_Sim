import pytest

from metro_sim.persistence.json_save_reader import read_json_file


def test_read_json_file_rejects_empty_file(tmp_path):
    path = tmp_path / "empty.json"
    path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="empty"):
        read_json_file(path)


def test_read_json_file_rejects_invalid_json(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{ broken", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON"):
        read_json_file(path)


def test_read_json_file_reads_valid_json(tmp_path):
    path = tmp_path / "valid.json"
    path.write_text('{"ok": true}', encoding="utf-8")

    data = read_json_file(path)

    assert data == {"ok": True}