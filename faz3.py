import math
import string
from collections import Counter
from difflib import SequenceMatcher
from numpy import dot
from numpy.linalg import norm
import json



def dot_product(vec1, vec2):
    return sum(val1 * val2 for val1, val2 in zip(vec1, vec2))


def magnitude(vector):
    return math.sqrt(sum(val**2 for val in vector))


def cosine_similarity(vec1, vec2):
    dot_prod = dot_product(vec1, vec2)
    mag_vec1 = magnitude(vec1)
    mag_vec2 = magnitude(vec2)
    
    if mag_vec1 != 0 and mag_vec2 != 0:
        return dot_prod / (mag_vec1 * mag_vec2)
    else:
        return 0 

def most_similar_word(word, word_dict):
    max_ratio = 0
    similar_word = ''

    for dict_word in word_dict.keys():
        seq_matcher = SequenceMatcher(None, word, dict_word)
        similarity_ratio = seq_matcher.ratio()

        if similarity_ratio > max_ratio:
            max_ratio = similarity_ratio
            similar_word = dict_word
    # print(max_ratio)
    if max_ratio > 0.8:
        return similar_word
    else:
        return ''


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
            

    return sum_vectors

def tf_p(documents,word_count,words,prepositions):
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
    
    # print(vectors)
    for i in range(len(words)):
        s = 0
        for j in range(len(vectors)):
            s += vectors[j][i]
        sum_vectors.append(s)
            
    # print(sum_vectors)
    return sum_vectors

def idf(documents,word_count,words,prepositions):
    vector = [0] * len(words)
    for w in word_count.keys():
        c = 0
        for paragragh in documents:
            # print(w)
            if w in paragragh and w not in prepositions:
                c += 1
        if c != 0:
            vector[words[w]] = math.log10(410837 / c)

    return vector


with open('data.json', 'r') as file:
    data = json.load(file)

for p in range(0,10):
    lis = data[p]["candidate_documents_id"]

    read_list = []
    with open('dt.txt', 'r') as file:
        content = file.read()

    content = content.split('\n')
    results = []

    for z in lis:    
        with open(f'data/document_{z}.txt', 'r',encoding='utf-8', errors='ignore') as file:
            text = file.read().lower()
            text = text.translate(str.maketrans('', '', string.punctuation))    

        tf_idf = [float(item) for item in content[z].split()]
        tf_idf.pop()

        prepositions = ['aboard', 'about', 'above', 'across', 'after', 'against', 'along', 'amid', 'among', 'around', 'as',
                    'at', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'but', 'by', 'concerning',
                    'considering', 'despite', 'down', 'during', 'except', 'following', 'for', 'from', 'in', 'inside', 'into',
                    'like', 'near', 'of', 'off', 'on', 'onto', 'out', 'outside', 'over', 'past', 'regarding', 'round',
                    'since', 'through', 'throughout', 'to', 'toward', 'under', 'underneath', 'until', 'unto', 'up',
                    'upon', 'with', 'within', 'without','the','a','or','which','where','per','and','are','most','its','an','that','be','is','may','it']

        query = data[p]["query"]

        documents = text.splitlines()


        all_words = ' '.join(documents).split()
     
        word_count = Counter(all_words)
    
        words = {}
        i = 0
        for word in word_count.keys():
            if word not in prepositions:
                words[word] = i
                i += 1
        query_without_punctuation = query.translate(str.maketrans('', '', string.punctuation))
        query_without_punctuation=query_without_punctuation.lower()

        query = ''
        
        
        for query_word in query_without_punctuation.split():
            if query_word not in prepositions:
                query += most_similar_word(query_word, words) + " "
        word_count = Counter(query.split())


        tf_vector = tf([query],word_count,words,prepositions)
        idf_vector = idf([query],word_count,words,prepositions)

        total_query_vector = []
        for i in range(int(len(words))):
            total_query_vector.append(tf_vector[i] * idf_vector[i])

        results.append((cosine_similarity(total_query_vector, tf_idf),z))
      
    sorted_list = sorted(results, key=lambda x: x[0])

    selected_doc=sorted_list[-1][1]
    print(selected_doc)

    with open(f'data/document_{selected_doc}.txt', 'r',encoding='utf-8', errors='ignore') as file:
        text = file.read().lower() 

        text = text.translate(str.maketrans('', '', string.punctuation)) 

    documents = text.splitlines()

    all_words = ' '.join(documents).split()

    word_count = Counter(all_words)

    words = {}
    i = 0
    for word in word_count.keys():
        if word not in prepositions:
            words[word] = i
            i += 1

    paragraph_similarity = []
    for line in documents:

        word_count = Counter(line.split())
    
        tf_paragraph=tf_p([line],word_count,words,prepositions)
        idf_paragraph=idf([line],word_count,words,prepositions)

        total_vector = []
        for i in range(len(idf_paragraph)):

            total_vector.append(tf_paragraph[i] * idf_paragraph[i])

        paragraph_similarity.append(cosine_similarity(total_query_vector,total_vector))

    print(paragraph_similarity.index(max(paragraph_similarity)))
    print()