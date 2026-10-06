"""
db.py — MongoDB connection helper.

Credentials are read from the environment (or a local, git-ignored `.env`
file). Nothing secret is ever stored in the source tree.

Required:
    MONGO_URI        Atlas / MongoDB connection string
Optional:
    MONGO_DB_NAME    Database name (default: fitcheck_women)
"""

import os

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

DEFAULT_DB_NAME = "fitcheck_women"


class MissingConfigError(RuntimeError):
    """Raised when a required environment variable is not set."""


def get_mongo_uri() -> str:
    uri = os.environ.get("MONGO_URI", "").strip()
    if not uri:
        raise MissingConfigError(
            "MONGO_URI is not set. Copy .env.example to .env and fill in your "
            "MongoDB connection string (or pass it as an environment variable)."
        )
    return uri


def _client_kwargs(uri: str) -> dict:
    kwargs = {"server_api": ServerApi("1")}
    # Only pin the CA bundle for TLS connections (Atlas "mongodb+srv://" URIs).
    # Certificate validation stays ON.
    if uri.startswith("mongodb+srv://") or "tls=true" in uri.lower():
        kwargs["tls"] = True
        kwargs["tlsCAFile"] = certifi.where()
    return kwargs


def get_client() -> MongoClient:
    uri = get_mongo_uri()
    return MongoClient(uri, **_client_kwargs(uri))


def get_collection(name: str):
    """Return a collection from the configured database."""
    db_name = os.environ.get("MONGO_DB_NAME", DEFAULT_DB_NAME)
    return get_client()[db_name][name]
