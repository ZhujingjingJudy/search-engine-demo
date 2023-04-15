"""configure initialization."""
import pathlib


# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'
SEARCH_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DATABASE_FILENAME = SEARCH_ROOT/'var'/'search.sqlite3'
