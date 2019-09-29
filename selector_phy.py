import spacy
from cleaner import secondary
import nltk
from nltk.corpus import stopwords
import re
import numpy as np
import sys
import json

class Selector():
    def __init__(self):
        self.discourse_connectives = {'Moreover', 'In addition', 'Additionally', 'Further', 'Further to this',
        'Also', 'Besides', 'What is more', 'However', 'On the other hand', 'In contrast', 'Yet', 'Although',
        'Even though', 'Despite the fact that', 'In spite of the fact that', 'Regardless of the fact that', 
        'Because', 'Since', 'As', 'Insofar as', 'Therefore', 'Consequently', 'In consequence', 
        'As a result', 'Accordingly', 'Hence', 'Thus', 'For this reason', 'Because of this', 
        'If', 'In the event of', 'As long as', 'So long as', 'Provided that', 'Assuming that', 'Given that', 
        'On the contrary', 'As a matter of fact', 'In fact', 'Indeed'}

        self.weights = [1, # 'first_sentence'
                        8, # 'word_scores'
                        2, # 'abbr'
                        10, # 'supr'
                        3, # 'pos'
                        -2, # 'discourse connectives'
                        8, # 'nouns_prons'
                        30, # ner detection
                        20] # equative detection

        self.stops = set(stopwords.words('english'))

        self.nlp = spacy.load('en_core_web_sm')

        self.threshold = 5 # 65

    def reader(self, filename):
        # print(secondary(filename))
        return secondary(filename)

    def word_scores(self, sent, counts):
        # y = sorted(counts.keys(), key = lambda i: -1*counts[i])
        trimmed = []
        for tok in counts.keys():
            if tok not in self.stops:
                if tok not in ['\n', '.', ',', '(', ')', ' ']:
                    trimmed.append(tok)
        toks = self.nlp(sent)
        summed_score = 0.0
        for tok in toks:
            if str(tok.lemma_) in trimmed:
                summed_score += counts[str(tok.lemma_).lower().strip()]/sum(counts.values())
        if summed_score!=0:
            return -1*np.log(summed_score)
        else:
            return -1*np.log(0.000000001)

    def discourse_connective(self, sentence):
        flag = 1
        for connective in self.discourse_connectives:
            if ' '.join(sentence.split()[:len(connective.split())]) == connective:
                flag = 0
                break
        return flag

    def abbr(self, sentence):
        x = re.findall(r'\b(?:[A-Z][a-z]*){2,}', sentence)
        return len(x)

    def superl(self, sentence):
        temp_text = nltk.word_tokenize(sentence)
        t = nltk.pos_tag(temp_text)
        count_super = 0
        for tag in t:
            # print(tag)
            if tag[1] == 'JJS' or tag[1] == 'RBS':
                count_super +=1
        return count_super

    def sentence_position(self, sentence, index_sentence, total):
        return index_sentence/total

    def num_nouns_pron(self, sentence):
        set_noun = set(['NN', 'NNS', 'NNP', 'NNPS'])
        set_pron = set(['PRP', 'PRP$', 'WP', 'WP$'])
        temp_text = nltk.word_tokenize(sentence)
        t = nltk.pos_tag(temp_text)
        c = 0
        for tag in t:
            if tag[1] in set_noun:
                c += 1
            if tag[1] in set_pron:
                c -= 5
        return c

    def ner_detection(self, s):
        s = s.strip()
        # s = ' '.join(s.split('\t'))
        s = self.nlp(s)
        return len(s.ents)

    def check_equative(self, s):
        pos = nltk.word_tokenize(str(s))
        pos = nltk.pos_tag(pos)
        start = 1
        for tag in pos:
            if start==1 and (tag[1] == 'NN' or tag[1] == 'NNS' or tag[1] == 'NNP'):
                start=2
            if start==2 and (tag[1] == 'VBZ' or tag[1] == 'VB' or tag[1] == 'VBP'):
                start=3
            if start==3 and (tag[1] == 'NN' or tag[1] == 'NNS' or tag[1] == 'NNP'):
                # print(s)
                start=4
                break
        if start==4:
            return 1
        return 0

    def score(self, sents):
        toks = []
        for sent in sents:
            toks+=[str(tok.lemma_).lower().strip() for tok in self.nlp(sent)]

        counts = {}
        for tok in toks:
            try:
                counts[tok] += 1
            except:
                counts[tok] = 1

        scores = []
        for i, sent in enumerate(sents):
            # sent = input("enter a sentence: ")

            features = [0]*9

            if i==1:
                features[0] = 1

            features[1] = self.word_scores(sent, counts)

            features[2] = self.abbr(sent)

            features[3] = self.superl(sent)

            features[4] = self.sentence_position(sent, i, len(sents))
            
            features[5] = self.discourse_connective(sent)

            features[6] = self.num_nouns_pron(sent)

            features[7] = self.ner_detection(sent)

            features[8] = self.check_equative(sent)

            scores.append(sum([self.weights[i]*features[i] for i in range(len(self.weights))])/len([t for t in self.nlp(sent)]))
            # print(features, scores[-1])
        
        return scores

    def generate_selections(self, filename):
        sentences = self.reader(filename) 
        print(len(sentences))
        scores = self.score(sentences)
        
        selections = []
        for i, s in enumerate(scores):
            if s >= self.threshold:
                selections.append(sentences[i])
        return selections

    def generate_json_bio(self, sen_list):
        d = []
        for sen in sen_list:
            s = sen
            ans_list = []
            sen = self.nlp(sen.strip())
            pos = nltk.word_tokenize(str(s))
            pos = nltk.pos_tag(pos)

            for X in sen.ents:
                ans_list.append(X.text)
            if len(ans_list)>0:
                c = {"text":s.strip() , "fibs":ans_list}
                d.append(c)
        return d


if __name__=='__main__':
    selector = Selector()
    selections = selector.generate_selections(sys.argv[1])

    d = selector.generate_json_bio(selections)
    print(len(d))

    with open(sys.argv[2], 'w') as f:
        f.write(json.dumps(d))
