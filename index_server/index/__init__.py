"""initialization"""
import os
import flask # noqa: E402  pylint: disable=wrong-import-position

app = flask.Flask(__name__)
import index.api

# Load inverted index, stopwords, and pagerank into memory
# FIXME:

index.api.index_load()
