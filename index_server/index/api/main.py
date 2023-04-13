"""api request methods."""
from pathlib import Path
from collections import defaultdict
import math
import re
import os
import flask
import index

SW = set()
PR = {}


def init():
    """Initialize the inverted index."""
    index.app.config["INDEX_PATH"] = os.getenv(
        "INDEX_PATH", "inverted_index_1.txt"
    )

    with open(
        "index_server/index/stopwords.txt", "r", encoding="UTF-8"
    ) as file:
        global SW
        SW = set([line.strip() for line in file.readlines()])

    with open(
        "index_server/index/pagerank.out", "r", encoding="UTF-8"
    ) as file:
        global PR
        lines = file.readlines()
        for line in lines:
            line = line.split(",")
            line = [word.strip() for word in line]
            PR[int(line[0])] = float(line[1])


@index.app.route("/api/v1/", methods=["GET"])
def get_page():
    """Get the page."""
    context = {"hits": "/api/v1/hits", "url": "/api/v1/"}
    return flask.jsonify(**context), 200


@index.app.route("/api/v1/hits/", methods=["GET"])
def get_hits():
    """Get hits for a query."""
    q_res = flask.request.args.get("q", default="", type=str)
    w_res = flask.request.args.get("w", default=0.5, type=float)

    # clean query
    q_res = q_res.split()
    q_res = [re.sub(r"[^a-zA-Z0-9]+", "", word.strip()) for word in q_res]
    q_res = [word.lower() for word in q_res]
    q_res = [word for word in q_res if word not in SW]
    print(q_res)

    # open the index file
    term_dict = {}
    path_dir = "index_server/index/inverted_index"
    with open(
        Path(path_dir) / Path(index.app.config["INDEX_PATH"]),
        "r",
        encoding="UTF-8",
    ) as file:
        lines = file.readlines()
        for line in lines:
            line = line.split()
            line = [word.strip() for word in line]
            term_dict[line[0]] = (float(line[1]), line[2:])

    potential_docs = defaultdict(set)
    for word in q_res:
        if word in term_dict:
            for idx, val in enumerate(term_dict[word][1]):
                if idx % 3 == 0:
                    potential_docs[word].add(int(val))
        else:
            potential_docs[word] = set()

    # calculate set intersection of all keys in potential_docs
    docs = set.intersection(*[potential_docs[key] for key in potential_docs])

    # calculate query vector
    query = []
    for word in q_res:
        if word in term_dict:
            query.append(term_dict[word][0] * len(docs))
        else:
            query.append(0)

    doc_dict = defaultdict(list)
    for doc in docs:
        for word in q_res:
            if word in term_dict:
                for idx, val in enumerate(term_dict[word][1]):
                    if idx % 3 == 0 and int(val) == doc:
                        freq = int(term_dict[word][1][idx + 1])
                        norm_score = float(term_dict[word][1][idx + 2])
                        score = freq * term_dict[word][0]
                        doc_dict[(doc, norm_score)].append(score)
            else:
                doc_dict[(doc, 0)].append(0)

    # calculate the dot product of the query vector and the document vector
    scores_dict = {}
    for doc in doc_dict:
        score = sum([a * b for a, b in zip(query, doc_dict[doc])])
        scores_dict[doc] = score

    # computer normalized of the query vector
    query_norm = sum([x**2 for x in query]) ** 0.5

    pr_score = {}
    for doc in doc_dict:
        doc_id = doc[0]
        doc_norm = math.sqrt(float(doc[1]))
        den = query_norm * doc_norm
        num = scores_dict[doc]
        tf_idf = num / den
        weight = w_res * PR[doc_id] + (1 - w_res) * tf_idf
        pr_score[doc_id] = weight

    context = {}
    context["hits"] = []
    # sort pr_score by value
    pr_score = {
        k: v
        for k, v in sorted(
            pr_score.items(), key=lambda item: item[1], reverse=True
        )
    }
    for doc in pr_score:
        context["hits"].append({"docid": doc, "score": pr_score[doc]})

    return flask.jsonify(**context), 200
