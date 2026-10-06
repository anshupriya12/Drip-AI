import pytest

import analyze_outfit as ao

SAMPLE = (
    "Style: Oversized denim jacket over a slip dress, strong silhouette. "
    "Rating: 72/100 "
    "Comment: Effortless, almost annoyingly so. "
    "Persona: Gen-Z"
)


def test_extractors():
    assert ao.extract_rating(SAMPLE) == pytest.approx(0.72)
    assert ao.extract_style_paragraph(SAMPLE).startswith("Oversized denim jacket")
    assert "Effortless" in ao.extract_comment(SAMPLE)
    assert ao.extract_persona(SAMPLE) == "Gen-Z"


def test_extractor_fallbacks():
    assert ao.extract_rating("no rating here") is None
    assert ao.extract_persona("Persona: unknown") == "Millennial"  # documented default


def test_importing_module_does_not_load_the_model():
    # Heavy models are loaded lazily; the cache must be empty after import.
    assert ao.load_model.cache_info().currsize == 0


def test_get_image_rejects_path_traversal(tmp_path, monkeypatch):
    monkeypatch.setattr(ao, "IMAGE_DIR", str(tmp_path / "Images"))
    (tmp_path / "Images").mkdir()
    (tmp_path / "secret.png").write_bytes(b"x")
    with pytest.raises(FileNotFoundError):
        ao.get_image("../secret.png")  # only the basename is used, so it is not found in Images/
