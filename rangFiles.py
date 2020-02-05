import numpy as np
import os
from parsingQueries import machingWord

d = 0.85    #dumping faktor

def findMatrixH(parsiraniFajlovi):
    H = np.eye(len(parsiraniFajlovi))  #ovo mi je H matrica
    H = H * 0   #svi elementi su mi 0 na pocetku
    for i, file in enumerate(parsiraniFajlovi, start = 0):
        for link in file.links:
            file.mapForH[os.path.basename(link)] += 1       #broj linkova u svakom fajlu prema ovom fajlu
        duzinaMape = 0
        for key in file.mapForH:
            duzinaMape += 1
        # print("Duzina mape: %s" %duzinaMape)
        # print("Broj Fajlova: %s" %len(parsiraniFajlovi))
        for j, key in enumerate(file.mapForH, start = 0):
            H[j, i] = file.mapForH[key]/len(file.links)     #punimo redove od matrice

    print(H)
    s = 0
    for i in range(len(H)):
        s += H[i,1]
    print(s)
    return H    #napravili smo matricu

def googleRankForFiles(H):
    n = len(H)
    v = np.ones(n)
    v /= n
    v = ((1-d)*v)
    v = np.transpose(v)  # pravimo vektor kolone
    print("Ovoooo je vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv ", v)

    return np.linalg.solve((np.eye(len(H))-d*H),v)     #hopefuly it works , treba da dobijemo vektor sa rangovima fajlova

def rangirajFajlovePoGooglu(parsiraniFajlovi):
    H = findMatrixH(parsiraniFajlovi)
    x = googleRankForFiles(H)
    for i, f in enumerate(parsiraniFajlovi, start = 0):
        f.googleRang = x[i]     #setujemo googlom rang


def RangFiles(searchedFiles, words, globalTrie):
    for file in searchedFiles:
        addRangToFile(file, words, globalTrie)

def addRangToFile(file, words, globalTrie):
    brojReciUFajlu = file.numberOfWord  #1. stavka ranga

    vrednostReciUDrugimFajlovima = 0
    for word in words:
        suc, docList = machingWord(word, globalTrie)
        if suc:
            for doc in docList:
                if os.path.abspath(file.file.name) in doc.file.links:
                     vrednostReciUDrugimFajlovima += doc.file.googleRang * doc.numberOfWord     #3. stavka ranga

    file.file.rang = brojReciUFajlu * file.file.googleRang*3 + vrednostReciUDrugimFajlovima     #dodeljujemo rang fajlu


def sortFilesByRang(pretrazeniFajlovi):  #algoritam za sortiranje po rangu
    if(len(pretrazeniFajlovi) == 0):
        print("Error")
    sortedFiles = pretrazeniFajlovi
    for i in range(0, len(sortedFiles)):
        for j in range(0, len(sortedFiles)):
            if sortedFiles[j].file.rang > sortedFiles[i].file.rang:
                sortedFiles[i], sortedFiles[j] = sortedFiles[j], sortedFiles[i] #ako je drugi veci menjamo mesta
    return sortedFiles