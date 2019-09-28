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


def get_refined_sentences(directory,filename,create_clean_file):
    if(create_clean_file):
        os.system("iconv -c -f utf-8 -t ascii "+directory+"/"+filename+" > "+directory+"/"+"clean-"+filename)


    with open(directory+"/"+"clean-"+filename) as f:
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
    for i,j in enumerate(refine1):
        print(i,j)
        
    return refine1

def main():
    directory="physics_data"
    filename="keph101.txt"
    create_clean_file=True
    refined=get_refined_sentences(directory,filename,create_clean_file)
