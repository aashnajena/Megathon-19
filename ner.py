import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import nltk

nlp = en_core_web_sm.load()

f = ['Firstly, I would like to say this']
for line in f:
	sent = nltk.sent_tokenize(line)
	for l in sent:
		print(l)
		l = nlp(l.rstrip())
		print([(X.text, X.label_) for X in l.ents] )
		for token in l:
		    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
		            token.shape_, token.is_alpha, token.is_stop)

