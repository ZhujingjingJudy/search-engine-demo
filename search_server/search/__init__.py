"""initialization."""
import flask

app = flask.Flask(__name__)
app.config["SEARCH_INDEX_SEGMENT_API_URLS"] = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]

# Read settings from config module (search/config.py)
app.config.from_object('search.config')
app.config.from_envvar("SEARCH_SETTINGS", silent=True)

import search.views  # noqa: E402  pylint: disable=wrong-import-position
import search.model  # noqa: E402  pylint: disable=wrong-import-position
