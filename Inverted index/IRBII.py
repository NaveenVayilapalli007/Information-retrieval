#!/usr/bin/env python
# coding: utf-8

#Import necessary libraries 
import sys
from os import listdir
from os.path import isfile, join
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize



#Preprocess the data(remove puntutations,convert to uppercase,get baseword etc)
ps = PorterStemmer()
def preprocessing(path,file_name):
        lines=[]
        f = open(path+"/"+file_name, "rb")
        for x in f:
            lines.append(str(x))
        no_lines = ""
        for sentence in lines:
            if sentence!='\n' and sentence!='':
                stop_words = set(stopwords.words('english'))
                words = word_tokenize(sentence)
                new_words= [word for word in words if word. isalnum()]
                stopword_removed_sentence = [w for w in new_words if not w in stop_words]
                mod_sentence = ""
                for word in stopword_removed_sentence:
                    mod_sentence+= ps.stem(word)+" "
                no_lines+=mod_sentence+'\n'
        return no_lines


#For removing the stopwords and punctuations in sentence
def RemoveStopWords(sentence):
        terms=[]
        for term in sentence.split() : 
            if term not in BRM.StopWords and term.isalnum() :
                terms.append(term)
        return terms

#to print the total terms with duplicates
def Terms(Data):
        Terms=[]
        for doc in Data:
            Terms.append(RemoveStopWords(Data[doc].upper()))
        Terms=[item for sublist in Terms for item in sublist]
        return Terms

#print Distinct Terms
def Distinctterms(Terms):
        DistinctTerms=[]
        for d in Terms :
            if d not in DistinctTerms:
                DistinctTerms.append(d)
        return DistinctTerms

#print Each Document terms
def DocumentColection(Data):
        DocCollect={}
        for doc in Data:
            if doc not in BRM.BooleanOperator :
                DocCollect[doc]=Distinctterms(RemoveStopWords(Data[doc].upper()))
        return DocCollect

"""#to print dictionary in better view
def displayDict(D):
        print("\n")
        for i in D:
            print (i , " : " ,D[i])
        print("\n")
"""

#to print dictionary for our view
def displayDiction(D):
        print("\n")
        for i in D:
            print (i ," ",D[i][0]," -----> " ,D[i][1:])
        print("\n")


class BRM:
    path="/home/christan/Desktop/IR_project_1/Inverted index/ShortStories"
    Data = {}
    onlyfiles = [f for f in listdir(path)]
    universal = [i for i in range(1,51)]
    for f in range(1,51):
        Data[f] = preprocessing(path,str(f)+".txt")
    StopWords = stopwords.words('english')
    BooleanOperator = {'AND', 'OR', 'NOT','and','or','not'}
    ## list of terms from the Data file collection
    TotalTerms=[]
    #list of Distinct Terms
    DistinctTerms=[]
    #Document collection terms
    EachDocumentTerms={}
    #inverted index
    invind = {}

    
#print("---  Text files content ---")
#displayDict(BRM.Data)

BRM.TotalTerms= Terms(BRM.Data)
#print ("\n--- Total Terms in docs ---\n" , *BRM.TotalTerms ,sep= " -- ")

BRM.DistinctTerms = Distinctterms(BRM.TotalTerms)
#print ("\n--- Distinct Terms in DOCs---\n", *BRM.DistinctTerms ,sep=" -- ")


BRM.EachDocumentTerms= DocumentColection(BRM.Data)
#print ("\n--- Each Document terms Collection ---" )
#displayDict(BRM.EachDocumentTerms)






#method for inverted index construction
def invind():
    temp={}
    for i in BRM.DistinctTerms:
        l=[]
        for j in range(1,51):
            if i in BRM.EachDocumentTerms[j]:
                l.append(j)
                temp[i]=l
        freq = len(temp[i])
        temp[i] = [freq,*temp[i]]
    return temp


invind = invind()
invind = dict(sorted(invind.items(), key=lambda x: (x[0],x[1][1])) )
displayDiction(invind)   #to print terms and corresponding posting lists


# to retrieve corresponding posting list for that term
def invindterm(term):
    return invind[term][1:]



#for query preprocessing
def Queryfiltration(Query):
    Qterms=[]
    j=[]
    Q=Query.upper().split()
    for term in Q:
        j.append(ps.stem(term).upper())
    
    for Qterm in j:
        if Qterm in BRM.DistinctTerms or Qterm in BRM.BooleanOperator :
            Qterms.append(Qterm)
    return Qterms


#for intersection operation used in case of and operation
def intersect(p1,p2): 
    p1 = set(p1) 
    p2 = set(p2) 
    return (p1 & p2)


#for union operation used in case of or operation
def Union(p1, p2): 
    final_list = p1 + p2
    return final_list


#For Boolean Operations like and,or,not
def BooleanOperatorProcessing(BoolOperator,PrevV,NextV):
    result=[]
    if BoolOperator == "AND":
        result = intersect(PrevV,NextV)
    elif BoolOperator=="OR" :
        result = Union(PrevV,NextV)
    elif BoolOperator == "NOT":
        for b in BRM.universal:
            if b not in PrevV:
                result.append(b)
       
    return result


#main method for query evaluation
def QueryProcessing(Query):
    Bitwiseop=""
    Qyterms=Queryfiltration(Query)
    result=[]
    hasPreviousterm=False
    hasntOperation=False
    IncVicNexBool=[]
    IncVicPreBool=[]
    for term in Qyterms :
        print(term)
        print()
        if term not in BRM.BooleanOperator:
            if hasntOperation:
                if hasPreviousterm:
                    IncVicNexBool=BooleanOperatorProcessing("NOT",invindterm(term),IncVicNexBool)
                
                else :
                    IncVicPreBool=BooleanOperatorProcessing("NOT",invindterm(term),IncVicNexBool)
                    result=IncVicPreBool
                    hasPreviousterm = True

                    
                hasntOperation=False
                    
            elif  hasPreviousterm :
                IncVicNexBool=invindterm(term)
            else :
                IncVicPreBool=invindterm(term)
                result=IncVicPreBool
                hasPreviousterm=True   
                
            
        elif term =="NOT":
            hasntOperation=True
            
        else :
            Bitwiseop=term
                
        if  len(IncVicNexBool)!= 0  :
            result = BooleanOperatorProcessing(Bitwiseop,IncVicPreBool,IncVicNexBool)
            IncVicPreBool=result
            hasPreviousterm=True
            IncVicNexBool= []
   
    result = sorted(result)
    
    for i in result:
        print(i)


#some queries
Q1="travel and water and your"
Q2= "not travel and water"
Q3 = "travel and not water"
Q4 = "not travel and not water"


QueryProcessing(Q1)
print()
QueryProcessing(Q2)
print()
QueryProcessing(Q3)
print()
QueryProcessing(Q4)
print()




