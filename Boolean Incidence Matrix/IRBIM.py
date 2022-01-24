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
def preprocessing(file_name):
        file = open(file_name,'r')
        lines = file.read().split("\n")
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

#to print dictionary in better view
def displayDict(D):
        print("\n")
        for i in D:
            print (i , " : " ,D[i])
        print("\n")


#build up the term document incidence matrix for each distinct term
def TermDocumentIncidenceMatrix(DocumentTermsCollection ,DistinctTerms):
    TermDocMatrix={}
    for term in DistinctTerms:
        Vector=[]
        for c in DocumentTermsCollection:

            if term in DocumentTermsCollection[c]:
                Vector.append(1)
            else :
                Vector.append(0)

        TermDocMatrix[term]=Vector
    return TermDocMatrix


#to retrive the term document incidence vector for particular term
def TermIncidenceVector(term):
    return BRM.TermDocMatrix[term]

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


#For Boolean Operations
def BooleanOperatorProcessing(BoolOperator,PrevV,NextV):
    result=[]
    if BoolOperator == "AND":
        for a , b in zip(NextV,PrevV) :
            if a==1 and b==1 :
                result.append(1)
            else :
                result.append(0)
    elif BoolOperator=="OR" :
        for a,b in zip(NextV,PrevV) :
            if a==0 and b==0 :
                result.append(0)
            else :
                result.append(1)
    elif BoolOperator == "NOT":
        for b in PrevV :
            if b == 1 :
                result.append(0)
            else :
                result.append(1)
    return result


# query processing 
def QueryProcessing(Query):
    Bitwiseop=""
    Qyterms=Queryfiltration(Query)
    result=[]
    resultSet={}
    hasPreviousterm=False
    hasntOperation=False
    IncVicPreBool=[]
    IncVicNexBool=[]
    for term in Qyterms :
        print(term)
        print()
        if term not in BRM.BooleanOperator:
            if hasntOperation:
                if hasPreviousterm:
                    IncVicNexBool=BooleanOperatorProcessing("NOT",TermIncidenceVector(term),IncVicNexBool)
                
                else :
                    IncVicPreBool=BooleanOperatorProcessing("NOT",TermIncidenceVector(term),IncVicNexBool)
                    result=IncVicPreBool
                    hasPreviousterm = True

                    
                hasntOperation=False
                    
            elif  hasPreviousterm :
                    
                IncVicNexBool=TermIncidenceVector(term)
            else :
                    
                IncVicPreBool=TermIncidenceVector(term)
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
   
    
    for i,doc in zip(result,BRM.Data):
        print(i,BRM.Data[doc])
        resultSet[doc]=i
    return resultSet





class BRM:
    path="/home/christan/Desktop/IR_project_1"
    Data = {}
    onlyfiles = [f for f in listdir(path)]
    txt_files = filter(lambda x: x[-4:] == '.txt', onlyfiles)
    for f in txt_files:
        Data[f] = preprocessing(f)
    StopWords = stopwords.words('english')
    BooleanOperator = {'AND', 'OR', 'NOT','and','or','not'}
    ## list of terms from the Data file collection
    TotalTerms=[]
    #list of Distinct Terms
    DistinctTerms=[]
    #Document collection terms
    EachDocumentTerms={}
    #TermDocumentIncidenceMatrix 
    TermDocMatrix={}

print("---  Text files content ---")
displayDict(BRM.Data)

BRM.TotalTerms= Terms(BRM.Data)
print ("\n--- Total Terms in 5 docs ---\n" , *BRM.TotalTerms ,sep= " -- ")

BRM.DistinctTerms = Distinctterms(BRM.TotalTerms)
print ("\n--- Distinct Terms in 5 DOCs---\n", *BRM.DistinctTerms ,sep=" -- ")

BRM.EachDocumentTerms= DocumentColection(BRM.Data)
print ("\n--- Each Document terms Collection ---" )
displayDict(BRM.EachDocumentTerms)


#Update Atribute in BRM class
BRM.TermDocMatrix=TermDocumentIncidenceMatrix(BRM.EachDocumentTerms,BRM.DistinctTerms)


#print term document incidence matrix
displayDict(BRM.TermDocMatrix)



Q1="structure and semantic"
Q2="not semantic and structure"
Q3="not structure and semantic"
Q4="not structure and not semantic"



print("Query1 processing result ",QueryProcessing(Q1))
print()
print("Query2 processing result ",QueryProcessing(Q2))
print()
print("Query3 processing result ",QueryProcessing(Q3))
print()
print("Query4 processing result ",QueryProcessing(Q4))
print()

