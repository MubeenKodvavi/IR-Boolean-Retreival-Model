"""
Code by Mubeen Kodvavi
18K-1198 FAST NUCES
"""

from nltk import PorterStemmer, word_tokenize
import re


def read_positional_index():
    """
    reads positional index from a file and returns it
    Return type: dictionary
    """
    try:
        file = open('positionalIndex.txt', encoding='utf-8')
    except:
        # if file not present, returns NF indicating no file
        return 'NF'
    positional_index = {}
    currTerm = ""
    for line in file:
        line_words = line.split()
        line_len = len(line_words)
        if (line_len == 1):
            currTerm = line_words[0]
            positional_index[currTerm] = {}
        else:
            docID = int(line_words[0])
            positional_index[currTerm][docID] = []
            for i in range(1, line_len):
                positional_index[currTerm][docID].append(int(line_words[i]))
    return positional_index


def read_inverted_index():
    """
    reads inverted index from a file and returns it
    Returns dictionary
    """
    try:
        file = open('invertedIndex.txt', encoding='utf-8')
    except:
        # if file not present, returns NF indicating no file
        return 'NF'
    inverted_index = {}
    currTerm = ""
    for line in file:
        line_words = line.split()
        line_len = len(line_words)
        currTerm = line_words[0]
        inverted_index[currTerm] = []
        for i in range(1, line_len):
            pass
            inverted_index[currTerm].append(int(line_words[i]))
    return inverted_index


def AND(p1, p2):
    """
    input parameters:
    p1(list): positing list 1
    p2(list): posting list 2
    Performs intersection on input lists and returns common documents
    Returns list
    """
    len_p1, len_p2 = len(p1), len(p2)
    answer = []
    i, j = 0, 0
    while i != len_p1 and j != len_p2:
        if p1[i] == p2[j]:
            answer.append(p1[i])
            i += 1
            j += 1
        elif p1[i] < p2[j]:
            i += 1
        else:
            j += 1
    return answer


def OR(p1, p2):
    """
    input parameters:
    p1(list): positing list 1
    p2(list): posting list 2
    Performs union on input lists and returns all documents present in both lists
    Returns list
    """
    len_p1, len_p2 = len(p1), len(p2)
    answer = []
    i, j = 0, 0
    while i != len_p1 and j != len_p2:
        if p1[i] == p2[j]:
            answer.append(p1[i])
            i += 1
            j += 1
        elif p1[i] < p2[j]:
            answer.append(p1[i])
            i += 1
        else:
            answer.append(p2[j])
            j += 1

    while i < len_p1:
        answer.append(p1[i])
        i += 1
    while j < len_p2:
        answer.append(p2[j])
        j += 1
    return answer


def NOT(p):
    """
    input parameter:
    p(list): posting list
    Performs not operation and return posting list of documents not present in input list
    Returns list
    """
    len_p = len(p)
    answer = [x for x in range(1, 51)]
    i, j = 0, 0
    while j != len_p:
        if answer[i] == p[j]:
            answer.pop(i)
            j += 1
            continue
        elif answer[i] < p[j]:
            i += 1
        else:
            j += 1
    return answer


def proximity(p1, p2, k):
    """
    Input parameters:
    p1(dict): posting list with positions
    p2(dict): posting list with positions
    k(int): how many words apart
    Handles proximity queries
    Checks if any posting list has entry of same docID with k words apart
    Returns list of matching
    """
    answer = []
    for key in p1.keys():
        if key in p2.keys():
            for i in range(len(p1[key])):
                for j in range(len(p2[key])):
                    if abs(p2[key][j] - p1[key][i]) <= k + 1 and key not in answer:
                        answer.append(key)
    return answer


def process_query(query):
    """
        Input parameters:
        query(string): Raw query in form of string
        Parses query and performs all preprocessing operations on it
        Checks if it is a positional query or not, and applies logical operations in order to produce a result
            list of documents.
        Returns list of retreived documents.
    """
    inverted_index = read_inverted_index()
    positional_index = read_positional_index()
    if inverted_index == 'NF' or positional_index == 'NF':
        # if file not present, returns NF indicating no file
        return 'NF'
    is_positional = False
    if len(query) > 3:
        if (query[-2] == '/' or query[-3] == '/' or query[-4] == '/'):
            #identifying positional query
            is_positional = True
    # removing punctuations
    query = re.sub(r'[^\w\s]', '', query)
    # casefolding
    query = query.lower()
    query = query.replace('ã', 'a')
    query = query.replace('ª', 'a')
    query = word_tokenize(query)
    stemmer = PorterStemmer()

    if is_positional:
        # passes parameter to positional query and returns result
        k = int(query.pop())
        try:
            posting_one = positional_index[stemmer.stem(query[0])]
        except:
            posting_one = {}
        try:
            posting_two = positional_index[stemmer.stem(query[1])]
        except:
            posting_two = {}
        result = proximity(posting_one, posting_two, k)
        return result

    else:
        # executing simple boolean query
        term_documents = []
        operators = []
        i = 0
        while i < len(query):
            if (query[i] == 'and' or query[i] == 'or'):
            # add to operators if and or or
                operators.append(query[i])
                i += 1
            elif query[i] == 'not':
                # perform not operation and add posting list to term documents
                j = i + 1
                not_words = []
                while query[j] != 'and' and query[j] != 'or':
                    not_words.append(query[j])
                    j += 1
                    if j == len(query):
                        break
                try:
                    posting = inverted_index[stemmer.stem(not_words[0])]
                except:
                    posting = []
                term_documents.append(NOT(posting))
                i += 2
            else:
                # adds posting list of word to term documents
                term = []
                j = i
                while query[j] != 'and' and query[j] != 'or':
                    term.append(query[j])
                    j += 1
                    if j == len(query):
                        break
                try:
                    posting = inverted_index[stemmer.stem(term[0])]
                except:
                    posting = []
                term_documents.append(posting)
                i += 1
        while (operators):
            operator = operators.pop(0)
            posting_one = term_documents.pop(0)
            posting_two = term_documents.pop(0)
            if (operator == 'and'):
                term_documents.insert(0, AND(posting_one, posting_two))
            elif (operator == 'or'):
                term_documents.insert(0, OR(posting_one, posting_two))
        return term_documents[0]


if __name__ == '__main__':
    """
        Runs as console application when script run independently
    """
    query = input("Enter your query:")
    print(process_query(query))
