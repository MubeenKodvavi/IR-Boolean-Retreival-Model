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
stemmer = nltk.PorterStemmer()
positional_index = {}
for file in os.listdir(stories_dir):
    story_file = open(stories_dir + file, encoding='utf-8')
    story = story_file.read()
    story_file.close()
    story = re.sub(r'[^\w\s]', '', story)
    docID = int(os.path.splitext(file)[0])
    tokens = nltk.word_tokenize(story)
    normalized_tokens = []
    number_of_tokens = len(tokens)
    for i in range(number_of_tokens):
        # casefolding
        tokens[i] = tokens[i].lower()
        # removing stop words
        if tokens[i] in stopwords:
            continue
        # removing dialects
        tokens[i] = tokens[i].replace('ã', 'a')
        tokens[i] = tokens[i].replace('ª', 'a')
        # stemming with Porter Stemmer
        tokens[i] = stemmer.stem(tokens[i])
        if positional_index.get(tokens[i]):
            if positional_index[tokens[i]].get(docID):
                if (i not in positional_index[tokens[i]][docID]):
                    positional_index[tokens[i]][docID].append(i + 1)
            else:
                positional_index[tokens[i]][docID] = []
                positional_index[tokens[i]][docID].append(i + 1)
        else:
            positional_index[tokens[i]] = {}
            positional_index[tokens[i]][docID] = []
            positional_index[tokens[i]][docID].append(i + 1)

# Sorting positional index
positional_index = {
    key: value
    for key, value in sorted(positional_index.items(), key=lambda a: a[0])
}

#Sorting positional index values
for key in positional_index.keys():
    positional_index[key] = {
        k: sorted(v)
        for k, v in sorted(positional_index[key].items(), key=lambda a: a[0])
    }

# Writing positional index to file
positional_file = open('positionalIndex.txt', 'w', encoding = 'utf-8')
for key, value in positional_index.items():
    positional_file.write("{}\n".format(key))
    for doc, positions in value.items():
        positional_file.write("{} ".format(doc))
        for position in positions:
            positional_file.write("{} ".format(position))
        positional_file.write("\n")