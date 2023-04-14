"""API function"""
from pathlib import Path
from collections import defaultdict
import math
import re
import os
import flask
import index
gStopWordsList = set()
pageRanks = {}


def index_load():
    """Load data from file"""
    index.app.config["INDEX_PATH"] = os.getenv(
        "INDEX_PATH", "inverted_index_1.txt"
    )
    with open(
        "index/stopwords.txt", "r", encoding="UTF-8"
    ) as file:
        global gStopWordsList
        for line in file.readlines():
            word = line.strip()
            gStopWordsList = set(word)
    file.close()

    with open("index/pagerank.out", "r", encoding="UTF-8") as file:
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
    path="index/inverted_index"
    with open(
        Path(path)/Path(index.app.config["INDEX_PATH"]),
        'r',"encoding=UTF-8") as f:
        lines=f.readlines()
        for line in lines:
            line.strip()
            line=line.split()
            term_dic[line[0]]={"idf":line[1],
                               "rest": line[2,:]}
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
                tfindex=doc*3+1
                tfI=result["rest"][tfindex]
                doc_vector[doc].append(idf*tfI)
            else:
                print("conflict, checpoint 106")        
    # for i in range((len(pageRanks))):
    #     doc_vector[i]=[]
    #     if i in union_docs:
    #         for query_term in query_list:
    #             if query_term in term_dic:
    #                 result=term_dic[query_term]
    #                 idf=float(result["idf"])
    #                 # term may appear in doc-i
    #                 docidList=result["rest"][0::3]
    #                 if i in docidList:
    #                     index_i=result["rest"].index(i)
    #                     index_i+=1
    #                     tf=result["rest"][index_i]
    #                     doc_vector[i].append(tf*idf)
    #                 else:
    #                     # doc_id = i, not contain this query_term  
    #                     doc_vector[i].append(0)
    #             else:
    #                 # none of doc contain this query_term
    #                 doc_vector[i].append(0)
    #     else:
    #         # none of doc contain any of query_term, all tf=0
    #         doc_vector[i]=[0]*len(query_list)
                    
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
    q_norm=math.sqrt(q_norm)
                
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
        context.append{"docid":key,
                       "score":value
            }
    return flask.jsonify(**context), 200
            
                
         

        
    
    
            
        
            
            
    
    
# FIXME:
# """api request methods."""
# from pathlib import Path
# from collections import defaultdict
# import math
# import re
# import os
# import flask
# import index

# SW = set()
# PR = {}


# def index_load():
#     """Initialize the inverted index."""
#     index.app.config["INDEX_PATH"] = os.getenv(
#         "INDEX_PATH", "inverted_index_1.txt"
#     )
#     print(os.getcwd())
#     with open(
#         "index/stopwords.txt", "r", encoding="UTF-8"
#     ) as file:
#         global SW
#         SW = set([line.strip() for line in file.readlines()])

#     with open(
#         "index/pagerank.out", "r", encoding="UTF-8"
#     ) as file:
#         global PR
#         lines = file.readlines()
#         for line in lines:
#             line = line.split(",")
#             line = [word.strip() for word in line]
#             PR[int(line[0])] = float(line[1])


# @index.app.route("/api/v1/", methods=["GET"])
# def get_page():
#     """Get the page."""
#     context = {"hits": "/api/v1/hits", "url": "/api/v1/"}
#     return flask.jsonify(**context), 200


# @index.app.route("/api/v1/hits/", methods=["GET"])
# def get_hits():
#     """Get hits for a query."""
#     q_res = flask.request.args.get("q", default="", type=str)
#     w_res = flask.request.args.get("w", default=0.5, type=float)

#     # clean query
#     q_res = q_res.split()
#     q_res = [re.sub(r"[^a-zA-Z0-9]+", "", word.strip()) for word in q_res]
#     q_res = [word.lower() for word in q_res]
#     q_res = [word for word in q_res if word not in SW]
#     print(q_res)

#     # open the index file
#     term_dict = {}
#     path_dir = "index_server/index/inverted_index"
#     with open(
#         Path(path_dir) / Path(index.app.config["INDEX_PATH"]),
#         "r",
#         encoding="UTF-8",
#     ) as file:
#         lines = file.readlines()
#         for line in lines:
#             line = line.split()
#             line = [word.strip() for word in line]
#             term_dict[line[0]] = (float(line[1]), line[2:])

#     potential_docs = defaultdict(set)
#     for word in q_res:
#         if word in term_dict:
#             for idx, val in enumerate(term_dict[word][1]):
#                 if idx % 3 == 0:
#                     potential_docs[word].add(int(val))
#         else:
#             potential_docs[word] = set()

#     # calculate set intersection of all keys in potential_docs
#     docs = set.intersection(*[potential_docs[key] for key in potential_docs])

#     # calculate query vector
#     query = []
#     for word in q_res:
#         if word in term_dict:
#             query.append(term_dict[word][0] * len(docs))
#         else:
#             query.append(0)

#     doc_dict = defaultdict(list)
#     for doc in docs:
#         for word in q_res:
#             if word in term_dict:
#                 for idx, val in enumerate(term_dict[word][1]):
#                     if idx % 3 == 0 and int(val) == doc:
#                         freq = int(term_dict[word][1][idx + 1])
#                         norm_score = float(term_dict[word][1][idx + 2])
#                         score = freq * term_dict[word][0]
#                         doc_dict[(doc, norm_score)].append(score)
#             else:
#                 doc_dict[(doc, 0)].append(0)

#     # calculate the dot product of the query vector and the document vector
#     scores_dict = {}
#     for doc in doc_dict:
#         score = sum([a * b for a, b in zip(query, doc_dict[doc])])
#         scores_dict[doc] = score

#     # computer normalized of the query vector
#     query_norm = sum([x**2 for x in query]) ** 0.5

#     pr_score = {}
#     for doc in doc_dict:
#         doc_id = doc[0]
#         doc_norm = math.sqrt(float(doc[1]))
#         den = query_norm * doc_norm
#         num = scores_dict[doc]
#         tf_idf = num / den
#         weight = w_res * PR[doc_id] + (1 - w_res) * tf_idf
#         pr_score[doc_id] = weight

#     context = {}
#     context["hits"] = []
#     # sort pr_score by value
#     pr_score = {
#         k: v
#         for k, v in sorted(
#             pr_score.items(), key=lambda item: item[1], reverse=True
#         )
#     }
#     for doc in pr_score:
#         context["hits"].append({"docid": doc, "score": pr_score[doc]})

#     return flask.jsonify(**context), 200
