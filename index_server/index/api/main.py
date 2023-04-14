"""API function"""
from pathlib import Path
from collections import defaultdict
import math
import re
import os
import flask
import index
from index import app
gStopWordsList = set()
pageRanks = {}


def index_load():
    """Load data from file"""
    with open(
        "index_server/index/stopwords.txt", "r", encoding="UTF-8"
    ) as file:
        global gStopWordsList
        for line in file.readlines():
            word = line.strip()
            gStopWordsList = set(word)
    file.close()

    with open("index_server/index/pagerank.out", "r", encoding="UTF-8") as file:
        global pageRanks
        for line in file.readlines():
            line = line.strip()
            page_id, pagerank = line.split(",")
            pageRanks[int(page_id)] = float(pagerank)
            
    file.close()


@index.app.route("/api/v1/", methods=["GET"])
def get_page():
    """Simple page."""
    context = {"hits": "/api/v1/hits",
               "url": "/api/v1/"
               }
    return flask.jsonify(**context), 200


@index.app.route("/api/v1/hits/", methods=["GET"])
def get_hits():
    """Query hit calc"""
    query = flask.request.args.get('q')
    weight = flask.request.args.get('w', default=0.5)

    # TODO: clean the query
    query = query.strip()
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    query = query.casefold()
    query = query.split()
    query_list = [term for term in query if term not in gStopWordsList]
    print(query_list)
    
    # TODO: calculation
    # -1 query vector
    #    -1 look up value for each term
    # FIXME: what about repeated query terms
    term_dic={}
    path="index_server/index/inverted_index"
    index_path = os.path.join(path, app.config["INDEX_PATH"])
    with open(index_path, "r", encoding="UTF-8") as f:
        lines=f.readlines()
        for line in lines:
            line.strip()
            line=line.split()
            term_dic[line[0]]={"idf":line[1],
                               "rest": line[2:]}
    query_vector=[]
    for query_term in query_list:
        if query_term in term_dic:
            result=term_dic[query_term]   
            value=query_list.count(query_term)*float(result["idf"])
            query_vector.append(value)
        else:
            query_vector.append(0)
    
    
    docs_include_term=defaultdict(set)
    for query_term in query_list:
        if query_term in term_dic:
            result=term_dic[query_term]
            for index,val in enumerate(result["rest"]):
                if index%3==0:
                    docs_include_term[query_term].add(int(val))
        else:
            docs_include_term[query_term]=set()
            
    # find union document containing all the term
    docs_intersection=set()
    for doc in docs_include_term.values():
        docs_intersection=docs_intersection.intersection(doc)
            
    doc_vector={}
    for doc in docs_intersection:
        # this doc contains all the query term
        doc_vector[doc]=[]
        for query_term in query_list:
            if query_term in term_dic:
                result=term_dic[query_term]
                idf=result["idf"]
                docidlist=result["rest"][0::3]
                docindex=docidlist.index(doc)
                tfindex=docindex*3+1
                tfI=result["rest"][tfindex]
                doc_vector[doc].append(idf*tfI)
            else:
                print("conflict, checpoint 106")        
                    
    # TODO: compute tf-idf
    qd_dot_list={}
    for doc in (docs_intersection):
        sum=0
        for q in range(len(query_list)):
            sum+=query_list[q]*doc_vector[doc][q]
        qd_dot_list[doc]=sum
    
    # TODO: compute q_norm
    sum=0
    for q in query_vector:
        sum+=q*q
    q_norm=math.sqrt(sum)
                
    # TODO: fetch normalization factor
    doc_nf_list={}
    for doc in docs_intersection:
        for query_term in query_list:
            if query_term in term_dic:
                result=term_dic[query_term]
                docidlist=result["rest"][0::3]
                docindex=docidlist.index(doc)
                nfindex=doc*3+2
                doc_nf_list[doc]=result["rest"][nfindex]
                break
    # TODO: compute tf-idf
    tfIdf=defaultdict(float)
    for doc in docs_intersection:
        tfIdf[doc]=qd_dot_list[doc]/(q_norm*doc_nf_list[doc])
                    
    # TODO: weighted score
    scorelist={}
    for doc in docs_intersection:
        scorelist[doc] = float(weight* pageRanks(doc) +(1-weight) *tfIdf[doc])               
    sorted_score_list= dict(sorted(scorelist.items(), key=lambda item: item[1],reverse=True))       
    context={}
    context["hits"]=[]
    for key,value in sorted_score_list.items():
        context.append({"docid":key,
                       "score":value
            })
    return flask.jsonify(**context), 200