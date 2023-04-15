"""search views index."""
import threading
import heapq
import flask
import search
import requests
from search.config import SEARCH_INDEX_SEGMENT_API_URLS


@search.app.route('/', methods=['GET'])
def page():
    """Search server page."""
    query = flask.request.args.get('q', default=None, type=str)
    pagerank = flask.request.args.get('w', default=0.5, type=float)
    # disp_q = ""
    # disp_w = 0.5
    initial = True
    if query is None:
        initial = True
        context = {'documents': [], 'num_docs': 0,
                   'initial': initial, "query": "", "pagerank": 0.5}
        return flask.render_template("index.html", **context)
    initial = False
    results = [[] for _ in range(len(SEARCH_INDEX_SEGMENT_API_URLS))]
    thread0 = threading.Thread(target=connect_index,
                               args=(query, pagerank, 0, results))
    thread1 = threading.Thread(target=connect_index,
                               args=(query, pagerank, 1, results))
    thread2 = threading.Thread(target=connect_index,
                               args=(query, pagerank, 2, results))
    thread0.start()
    thread1.start()
    thread2.start()
    thread0.join()
    thread1.join()
    thread2.join()
    # result = [results[0]['hits'], results[1]['hits'], results[2]['hits']]
    # merge_result = heapq.merge(*results, key=get_score, reverse=True)
    doc_ids = []
    for doc in heapq.merge(*results, key=get_score, reverse=True):
        doc_ids.append(doc['docid'])
    num_docs = len(doc_ids)
    if num_docs > 10:
        new_ids = []
        for i in range(10):
            new_ids.append(doc_ids[i])
        doc_ids = new_ids
        num_docs = 10
    # connection = search.model.get_db()
    show_doc = []
    for i in range(num_docs):
        cur = search.model.get_db().execute(
            "SELECT * "
            "FROM Documents "
            "WHERE docid = ?",
            (doc_ids[i], )
            )
        show_doc.append(cur.fetchone())
    context = {'documents': show_doc, 'num_docs': num_docs,
               'initial': initial, "query": query, "pagerank": pagerank}
    return flask.render_template("index.html", **context)


def connect_index(qes, wid, index, results):
    """Connect index."""
    # url_param = {'q': q, 'w': w}
    url = f"{SEARCH_INDEX_SEGMENT_API_URLS[index]}?q={qes}&w={wid}"
    res = ""
    if qes != "":
        respond = requests.get(url, timeout=5)
        # try:
        #     r = requests.get(url, timeout=5)
        #     r.raise_for_status()
        # except requests.exceptions.HTTPError as err:
        #     raise SystemExit(err) from err
        res = respond.json()
        results[index] = res['hits']


def get_score(doc):
    """Get score."""
    return doc['score']
