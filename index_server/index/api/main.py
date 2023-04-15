"""API function."""
from collections import defaultdict
import math
import re
import os
import flask
import index
from index import app


def index_load():
    """Load data from file."""
    stopwords_list = set()
    page_ranks = {}
    with open(
        "index_server/index/stopwords.txt", "r", encoding="UTF-8"
    ) as file:
        stopwords_list = set(query_term.strip()
                             for query_term in file.readlines())
    file.close()

    with open("index_server/index/pagerank.out",
              "r", encoding="UTF-8") as file:
        for query_term in file.readlines():
            query_term = query_term.strip()
            i, temp = query_term.split(",")
            page_ranks[int(i)] = float(temp)
    file.close()
    return page_ranks, stopwords_list


@index.app.route("/api/v1/", methods=["GET"])
def get_page():
    """Get page."""
    context = {"hits": "/api/v1/hits",
               "url": "/api/v1/"
               }
    return flask.jsonify(**context), 200


@index.app.route("/api/v1/hits/", methods=["GET"])
def get_hits():
    """Query hit calc."""
    page_ranks, stopwords_list = index_load()
    query = flask.request.args.get('q')
    weight = flask.request.args.get('w', default=0.5)

    # Done: clean the query
    query = query.strip()
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    query = query.casefold().split()
    query = [query_term for query_term in query
             if query_term not in stopwords_list]

    # Done: calculation
    # -1 query vector
    #    -1 look up value for each term
    term_dic = {}
    with open(os.path.join("index_server/index/inverted_index",
                           app.config["INDEX_PATH"]),
              "r", encoding="UTF-8") as file:
        temp = file.readlines()
        term_dic = {i[0]: {"idf": i[1], "rest": i[2:]}
                    for i in (i.split(" ") for i in temp) if i[0] in query}

    query_vector = [query.count(query_term)*float(term_dic[query_term]["idf"])
                    if query_term in term_dic else 0 for query_term in query]

    doc = {query_term: {int(temp)
                        for i, temp in enumerate(term_dic[query_term]["rest"])
                        if i % 3 == 0}
           if query_term in term_dic else set() for query_term in query}

    # find union document containing all the term
    docs_intersection = set.intersection(
        *[doc[i] for i in doc])

    score_list = defaultdict(list)
    for doc in docs_intersection:
        # this doc contains all the query term
        for query_term in query:
            if query_term in term_dic:
                score_list[doc].append(float(
                    term_dic[query_term]["idf"])*float(
                    term_dic[query_term]["rest"][(
                        term_dic[query_term]["rest"][0::3].index(str(doc))
                        )*3+1]))
            else:
                print("conflict, checpoint 106")

    # compute tf-idf
    qd_dot_list = {}
    for doc in (docs_intersection):
        temp = 0
        for i, query_term in enumerate(query_vector):
            temp += float(query_term)*float(score_list[doc][i])
        qd_dot_list[doc] = temp

    # compute q_norm
    temp = sum(float(i) * float(i) for i in query_vector)

    # fetch normalization factor
    i = {}
    for doc in docs_intersection:
        for query_term in query:
            if query_term in term_dic:
                i[doc] = term_dic[query_term]["rest"][(
                    term_dic[query_term]["rest"][0::3].index(str(doc)))*3+2]
    # compute tf-idf
    query_vector = {}
    for doc in docs_intersection:
        query_vector[doc] = float(qd_dot_list[doc]) / \
            (math.sqrt(temp)*math.sqrt(float(i[doc])))

    # weighted score
    score_list = {}
    for doc in docs_intersection:
        score_list[doc] = float(weight)*float(page_ranks[doc]) + \
            (1-float(weight))*float(query_vector[doc])
    score_list = dict(
        sorted(score_list.items(), key=lambda item: item[1], reverse=True))
    doc = {}
    doc["hits"] = []
    for i, temp in score_list.items():
        doc["hits"].append({"docid": i,
                            "score": temp
                            })
    return flask.jsonify(**doc), 200
