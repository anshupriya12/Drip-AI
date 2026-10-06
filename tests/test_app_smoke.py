"""Smoke tests: every Streamlit page renders without exceptions.

MongoDB is replaced by an in-memory fake and the heavy models are never loaded
(they are only touched after a user uploads an image).
"""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

import db

DRIP = Path(__file__).resolve().parent.parent / "Drip"
PAGES = [
    DRIP / "Fashion AI Advisor.py",
    DRIP / "pages" / "1_Add_to_Inventory.py",
    DRIP / "pages" / "2_Get_Outfit_Suggestion.py",
]


class FakeCursor(list):
    def limit(self, n):
        return FakeCursor(self[:n])


class FakeCollection:
    def __init__(self, docs=None):
        self.docs = docs or []

    def count_documents(self, query):
        return len(self.docs)

    def find(self, *args, **kwargs):
        return FakeCursor(self.docs)

    def find_one(self, *args, **kwargs):
        return None

    def insert_one(self, doc):
        self.docs.append(doc)


@pytest.fixture(autouse=True)
def _clear_streamlit_caches():
    import streamlit as st

    st.cache_resource.clear()
    st.cache_data.clear()
    yield


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_page_renders_with_fake_db(page, monkeypatch):
    monkeypatch.setattr(db, "get_collection", lambda name: FakeCollection())
    at = AppTest.from_file(str(page), default_timeout=30).run()
    assert not at.exception, [e.value for e in at.exception]
    assert not at.error


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_page_shows_config_error_without_mongo_uri(page, monkeypatch):
    monkeypatch.delenv("MONGO_URI", raising=False)
    at = AppTest.from_file(str(page), default_timeout=30).run()
    assert not at.exception, [e.value for e in at.exception]
    assert any("MONGO_URI" in e.value for e in at.error)
