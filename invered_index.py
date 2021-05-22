"""
Code by Mubeen Kodvavi
18K-1198 FAST NUCES
"""

import nltk
import os
import re

# Storing a list of stopwords
stopwords_file = open('Stopword-List.txt', encoding='utf-8')
stopwords = []
for line in stopwords_file:
    for word in line.split():
        stopwords.append(word)
stopwords_file.close()

#Reading stories and PreProcessing
stories_dir = 'ShortStories/'
#using porterStemmer
stemmer = nltk.PorterStemmer()
inverted_index = {}
for file in os.listdir(stories_dir):
    #reads data file by file and process it in inverted index
    story_file = open(stories_dir + file, encoding='utf-8')
    story = story_file.read()
    story_file.close()
    story = re.sub(r'[^\w\s]', '', story)
    docID = int(os.path.splitext(file)[0])
    # tokenisation
    tokens = nltk.word_tokenize(story)
    normalized_tokens = []
    for token in tokens:
        token = token.lower()
        # removing accents and diacritics
        token = token.replace('ã', 'a')
        token = token.replace('ª', 'a')
        # removing stop words
        if (token in stopwords):
            continue
        # appending to normalized tokens
        normalized_tokens.append(stemmer.stem(token))
    for term in normalized_tokens:
        if (inverted_index.get(term)):
            if (docID not in inverted_index[term]):
                inverted_index[term].append(docID)
        else:
            inverted_index[term] = []
            inverted_index[term].append(docID)

# Sorting inverted index's terms and posting list
inverted_index = {
    key: sorted(val)
    for key, val in sorted(inverted_index.items(), key=lambda a: a[0])
}

# Writing inverted index to the dile
inverted_file = open('invertedIndex.txt', 'w', encoding='utf-8')
for key, value in inverted_index.items():
    inverted_file.write('{} '.format(key))
    for doc in value:
        inverted_file.write('{} '.format(doc))
    inverted_file.write('\n')
inverted_file.close()