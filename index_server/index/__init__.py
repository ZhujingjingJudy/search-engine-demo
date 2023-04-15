"""initialization."""

import os
import flask
app = flask.Flask(__name__)
app.config["INDEX_PATH"] = os.getenv(
    "INDEX_PATH", "inverted_index_1.txt"
)
import index.api  # noqa: C0413  pylint: disable=wrong-import-position
# Load inverted index, stopwords, and pagerank into memory

index.api.index_load()
