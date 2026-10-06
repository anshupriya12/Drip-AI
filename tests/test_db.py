import pytest

import db


def test_missing_uri_raises_clear_error(monkeypatch):
    monkeypatch.delenv("MONGO_URI", raising=False)
    with pytest.raises(db.MissingConfigError, match="MONGO_URI"):
        db.get_mongo_uri()


def test_blank_uri_is_treated_as_missing(monkeypatch):
    monkeypatch.setenv("MONGO_URI", "   ")
    with pytest.raises(db.MissingConfigError):
        db.get_mongo_uri()


def test_atlas_uri_enables_tls_and_never_disables_cert_validation():
    kwargs = db._client_kwargs("mongodb+srv://<user>:<password>@cluster.example.mongodb.net/")
    assert kwargs["tls"] is True
    assert "tlsCAFile" in kwargs
    assert "tlsAllowInvalidCertificates" not in kwargs


def test_plain_local_uri_does_not_force_tls():
    kwargs = db._client_kwargs("mongodb://localhost:27017")
    assert "tls" not in kwargs
