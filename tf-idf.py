import math
import string
from collections import Counter
import time

def tf(documents,word_count,words,prepositions):
    vectors = []
    for paragragh in documents:
        p_words = Counter(paragragh.split())
        vector = [0] * len(words)
        for w in paragragh.split():
            if w not in prepositions:
                tf_word = p_words[w] / len(word_count)
                vector[words[w]] = tf_word
        vectors.append(vector)
    sum_vectors = []

    for i in range(len(words)):
        s = 0
        for j in range(len(vectors)):
            s += vectors[j][i]
        sum_vectors.append(s)

    return sum_vectors , vectors

def idf(documents,word_count,words,prepositions):
    vector = [0] * len(words)
    for w in word_count.keys():
        c = 0
        for paragragh in documents:
            if w in paragragh and w not in prepositions:
                c += 1
        if c != 0:
            vector[words[w]] = math.log10(410837 / c)

    return vector
s = time.time()
data = []
for z in range(2):  
          
    with open(f'data/document_{z}.txt', 'r',encoding='utf-8', errors='ignore') as file:
        text = file.read().lower()  

        text = text.translate(str.maketrans('', '', string.punctuation))

        prepositions = ['aboard', 'about', 'above', 'across', 'after', 'against', 'along', 'amid', 'among', 'around', 'as',
                    'at', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'but', 'by', 'concerning',
                    'considering', 'despite', 'down', 'during', 'except', 'following', 'for', 'from', 'in', 'inside', 'into',
                    'like', 'near', 'of', 'off', 'on', 'onto', 'out', 'outside', 'over', 'past', 'regarding', 'round',
                    'since', 'through', 'throughout', 'to', 'toward', 'under', 'underneath', 'until', 'unto', 'up',
                    'upon', 'with', 'within', 'without','the','a','or','which','where','per','and','are','most','its','an','that','be','is','may','it']
    i = 0
    words = {}
    total_vector = []
    documents = text.splitlines()

    all_words = ' '.join(documents).split()

    word_count = Counter(all_words)

    for word in word_count.keys():
        if word not in prepositions:
            words[word] = i
            i += 1

    tf_vector,tf_paragraph_vector=tf(documents,word_count,words,prepositions)
    idf_vector=idf(documents,word_count,words,prepositions)

    for i in range(int(len(words))):
        total_vector.append(tf_vector[i] * idf_vector[i])

    with open("dat.txt",'a',encoding='utf-8', errors='ignore') as f:
        for item in total_vector:
            f.write(str(item) + " ")
        f.write('\n')

e = time.time()

print(e-s)