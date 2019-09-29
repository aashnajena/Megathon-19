# encoding: utf-8
from __future__ import unicode_literals
import re
import nltk
import requests
from nltk.parse.corenlp import CoreNLPDependencyParser
nltk.download('punkt')

# weights = {first_sentence : 1, sim_tok : 5, abbr : 1, supr : 3, pos : 2, ln : 1, nouns : 3, prn : 2}

discourse_connectives = ['Moreover', 'In addition', 'Additionally', 'Further', 'Further to this',
'Also', 'Besides', 'What is more', 'However', 'On the other hand', 'In contrast', 'Yet', 'Although', 
'Even though', 'Despite the fact that', 'In spite of the fact that', 'Regardless of the fact that', 
'Because', 'Since', 'As', 'Insofar as', 'Therefore', 'Consequently', 'In consequence',
'As a result', 'Accordingly', 'Hence', 'Thus', 'For this reason', 'Because of this',
'If', 'In the event of', 'As long as', 'So long as', 'Provided that', 'Assuming that', 'Given that',
'On the contrary', 'As a matter of fact', 'In fact', 'Indeed']

def freq_sim_tokens(sentence, dict_domain) :
    count = 0
    for word in sentence :
        if word in dict_domain :
            count+=1
    return count
def height_dependance(sentence):
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    parse, = dep_parser.raw_parse(sentence)
    parsed = parse.to_conll(3).split()
    scores=[]
    words=[]
    height=[]
    for i in range(0,len(parsed)-2,3):
        words.append(parsed[i])
        height.append(int(parsed[i+2]))
    max_height=max(height)
    for i in height:
        scores.append((max_height-i+1)/max_height)
    print(dict(zip(words,scores)))
def abbr(sentence):
    x = re.findall(r'\b(?:[A-Z][a-z]*){2,}', sentence)
    return len(x)

def superl(sentence):
    temp_text = nltk.word_tokenize(sentence)
    t = nltk.pos_tag(temp_text)
    count_super = 0
    for tag in t:
        # print(tag)
        if tag[1] == 'JJS' or tag[1] == 'RBS':
            count_super +=1
    return count_super

def sentence_position(sentence, index_setence, list_sentence):
    return len(list_sentences)/index_setence

def discourse_connective(sentence):
    flag = 1
    for connective in discourse_connectives:
        if ' '.join(sentence.split()[:len(connective.split())]) == connective:
            flag = 0
            break
    return flag

def num_nouns_pron(sentence):
    list_noun_pron = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$', 'WP', 'WP$']
    temp_text = nltk.word_tokenize(sentence)
    t = nltk.pos_tag(temp_text)
    count_nouns_pron = 0
    for tag in t:
        if tag[1] in list_noun_pron:
            count_nouns_pron +=1
    return count_nouns_pron

# print(superl("This is the most USA someone can get in the smallest possible time."))
# print(discourse_connective("he dies"))

print(abbr("He is a good boy and she is a good girl."))