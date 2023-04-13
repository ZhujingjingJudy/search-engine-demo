import index.api
import flask  # noqa: E402  pylint: disable=wrong-import-position
app = flask.Flask(__name__)
# Load inverted index, stopwords, and pagerank into memory
# FIXME:
# index.api.load_index()
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")
