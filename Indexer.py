__author__ = 'Sneha'
import sys

#Command Line args
#scriptName = sys.argv[0]
inputFile = sys.argv[1]
outputFile = sys.argv[2]

input = open(inputFile,"r")
word_corpus = {}
count = 0
final_length_dict = {}
output = open(outputFile, "w")

for line in input:
    line = line.strip()
    if line.startswith("#"):
        content = line.split(" ")
        document_id = int(content[1])
    else:
        word = line.split(" ")
        store_len = 0
        store_len = word.__len__()
        if document_id in final_length_dict:
            final_length_dict[document_id] += store_len
        else:
            final_length_dict[document_id] = store_len
        for w in word:
            doc_count = {}
            if w not in word_corpus:
                doc_count[document_id] = 1
                word_corpus[w] = doc_count
            else:
                word_dict = word_corpus[w]
                if document_id in word_dict:
                    word_dict[document_id] += 1
                else:
                    word_dict[document_id] = 1

for w in word_corpus:
    string = w + "-"
    document_count = word_corpus[w]
    for d in document_count:
        string +=  str(d) + ";" + str(document_count[d]) + "+"
    string = string[:-1]
    output.write(string + "\n")
output.close()
