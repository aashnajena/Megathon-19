import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import nltk
import json

nlp = en_core_web_sm.load()

selected = 0
no = 0
# e = open('chem.txt','r')

f = open('kech103.txt','r')
l = [] 
# for line in e:
# 	l.append(line.split('.')[0])
# print(len(l))

s1 = []
for line in f:
	sent = nltk.sent_tokenize(line)
	for s in sent:
		flag=0
		s = s.strip()
		s = ' '.join(s.split('\t'))
		s = nlp(s.strip())
		for token in s:
			if (token.lemma_=='be' or token.tag_== 'VBZ' or token.tag_ == 'VB' or token.tag_ == 'VBP') and len(s.ents)>0:
				print(s)
				print([(X.text, X.label_) for X in s.ents] )
				flag=1
				selected +=1
				s1.append(s)
				break
		if flag==0:
			no += 1	
print(selected)
print(no)


# common = 0
# for sent in s1:
# 	if sent in l:
# 		print('common:')
# 		print(sent)
# 		common+=1

# print(common)		


