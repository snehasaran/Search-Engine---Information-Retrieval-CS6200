__author__ = 'Sneha'
import sys

inputFile = sys.argv[1]
#ndex_out.txt
queriesFile = sys.argv[2]
#queries.txt"
maximum = int(sys.argv[3])
#100
outputFile = sys.argv[4]
#results_eval.txt


input = open(inputFile , "r")
query_file = open(queriesFile, "r")
query1 = open(outputFile, "w")


query1.write("query_id        Q0       doc_id      rank        BM25_score       system_name"+"\n")
queries = []
for line in query_file:
    line = line.strip()
    queries.append(line)

word_corpus = {}
count = 0
final_length_dict = {}
import math
import operator
from collections import OrderedDict


word_corpus = {}
for line in input:
    line = line.strip()
    content = line.split("-")
    word = content[0]
    rest = content[1]
    key_val = rest.split("+")
    dict = {}
    for kv in key_val:
        key = int(kv.split(";")[0])
        value = int(kv.split(";")[1])
        dict[key] = value
    word_corpus[word] = dict
#print(word_corpus)

final_length_dict = {}

for w in word_corpus:
    document_count_dict = word_corpus[w]
    for d in document_count_dict:
        if d not in final_length_dict:
            final_length_dict[d] = document_count_dict[d]
        else:
            final_length_dict[d] += document_count_dict[d]

intermed_len = 0

for key in final_length_dict:
    intermed_len += final_length_dict[key]

totalkeys = final_length_dict.__len__()

#print(intermed_len)
#print(totalkeys)

#query = "portabl oper system"
query_id = 0
for query in queries:
    query_id += 1
    q_words = query.split(" ")
    # Word_docs is a dict of word and docs it occurs in
    word_docs = {}
    for w in q_words:
        if w in word_corpus:
            document_count_dict = word_corpus[w]
            docs_word = set()
            for dc in document_count_dict:
                docs_word.add(dc)
            word_docs[w] = docs_word
        else:
            word_docs[w] = None



    #for w in q_words:
    #    print(w + " ;" + str(word_docs[w]))

    ''' doc_id : bm25 '''
    bm25_inter = {}
    bm25 = {}
    word_count = {}
    # word_count is dict of word key and value is number of occurances in entire corpus
    for w in q_words:
        count = 0
        if w in word_corpus:
            document_count_dict = word_corpus[w]
            for d in document_count_dict:
                count += document_count_dict[d]
        else:
            count = 0
        word_count[w] = count

    k1 = 1.2
    k2 = 100
    b = 0.75
    avdl = intermed_len/float(totalkeys)
    dl = len(query)


    set_docs = set()
    for w in q_words:
        docs = word_docs[w]
        for d in docs:
            #print(d)
            set_docs.add(d)

    for d in set_docs:
        K = k1 * ((1-b) + (b * (final_length_dict[d] / float(avdl))))
        score = 0
        for w in q_words:
            qfi = q_words.count(w)
            ri =0
            R =0
            numerator = (ri + 0.5) / (R - ri + 0.5)
            document_count_dict = word_corpus[w]
            if d in document_count_dict:
                fi = document_count_dict[d]
            else:
                fi = 0
            term1 = ((k1 + 1) * fi) /(K + fi)
            #print("Document: "+ str(d) + " term1: "+ str(term1))
            term2 = ((k2 + 1) * qfi)/ (k2 + qfi)
            #print("Document: "+ str(d) + " term2: "+ str(term2))
            term3_nr = (ri + 0.5) / (R - ri + 0.5)
            #print("Document: "+ str(d) + " numerator: "+ str(numerator))
            term3_dn = (len(word_docs[w]) - ri + 0.5) / float ((len(final_length_dict) - len(word_docs[w]) - R + ri + 0.5))
            #print("Document: "+ str(d) + " denominator: "+ str(term3_dn))
            if (term3_nr > 0 and term3_dn > 0) or (term3_nr < 0 and term3_dn < 0):
                score += (math.log(term3_nr/term3_dn) *term1 * term2)
            else:
                score += 0
                #print("K: " + str (d) + " "+str(K))
        bm25[d] = score

    #for w in word_docs:
    #    print(w + ";" + str(word_docs[w]))

    #print(str(word_count))

    #print("Printing the bm25")
    # for d in bm25:
    #     #print(str(d) + ";" + str(bm25[d]))
    #     bm25_Scorelist.write(str(d) + ";" + str(bm25[d]))
    #     bm25_Scorelist.write("\n")

    top_25_dict = OrderedDict(sorted(bm25.items(), key=operator.itemgetter(1), reverse=True)[:maximum])
    rank_val = 1
    system_name = 'Sneha Saran'

    for elem in top_25_dict.keys():
        query1.write(str(query_id) + "                 " + "Q0" + "       " + str(elem) + "      " + str(rank_val) + "      "
                     + str(top_25_dict[elem]) + "      " + str(system_name))
        rank_val += 1
        query1.write("\n")
    append_line = "=================================================================================" + "\n"
    query1.write(append_line)








