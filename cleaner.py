# coding: utf-8

import re
import os

def multi_split(s, seprators):
    buf = [s]
    for sep in seprators:
        for loop, text in enumerate(buf):
            if sep in s:
                buf[loop:loop+1] = [i+sep for i in text.split(sep) if i]
            else:
                buf[loop:loop+1] = [i for i in text.split(sep) if i]
    return buf

def add_space(temp,i):
    #print(temp,i)
    if not temp.endswith(" ") and not i.startswith(" "):
        if temp != " ":
            return temp+" "+i
        else:
            return i
    else:
        if temp != " ":
            return temp+i
        else:
            return i


def get_refined_sentences(filename,create_clean_file):
    # if(create_clean_file):
    #     os.system("iconv -c -f utf-8 -t ascii "+directory+"/"+filename+" > "+directory+"/"+"clean-"+filename)


    with open(filename, encoding='ascii', errors='ignore') as f:
        data=f.read().splitlines() 
    data = list(filter(None, data))
    termination_punctuation=['?','.','!']        

    sentences=[]
    temp=str(data[0])
    for i in data[1::]:
        #print("end",i)
        if i[-1] in termination_punctuation:
            #print("select",i)
            temp=add_space(temp,i)
            sentences.append(temp)
            temp=""
            '''
        elif i[0].isupper() and i!=' ':
            print(temp,"end",i)
            sentences.append(temp)
            temp=i
            '''
        else:
            temp=add_space(temp,i)

    
    refine1=[]
    for i,j in enumerate(sentences):
        m = multi_split(j, termination_punctuation)
        for k in m:
            k=k.replace('\t','')
            refine1.append(k)

    return refine1

def secondary(filename, create_clean_file=True):
    refined2 = []
    refined=get_refined_sentences(filename,create_clean_file)
    unit = re.compile('^[0-9]')
    unit2 = re.compile('^[0-9].')
    for r in refined:
        fl=0
        if 'table' in r.lower() or 'problem' in r.lower() or 'fig' in r.lower():
            fl = 1
        if unit.search(r) or unit2.search(r):
            # print(r)
            fl = 1    
        # if 'exercise' in r.lower() or 'exercises' in r.lower():
        #     break     
        for word in r:
            if '?' in word or '!' in word:
                fl = 1
        if fl==0:
            refined2.append(r)
    # print (refined2)        
    return refined2        


# main()