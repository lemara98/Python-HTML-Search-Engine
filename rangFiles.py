from time import time

import numpy as np
import os
from parsingQueries import machingWord


d = 0.85    #dumping faktor

def findMatrixH(parsiraniFajlovi):
    H = np.eye(len(parsiraniFajlovi))  #ovo mi je H matrica
    H = H * 0   #svi elementi su mi 0 na pocetku
    vremeEx = 0
    vremeIs = 0
    mapaSvihMogucihLinkova = {}
    for pr in parsiraniFajlovi:
        mapaSvihMogucihLinkova[pr.name] = pr.name
    for i, file in enumerate(parsiraniFajlovi, start = 0):
        mapaPotrebnihLinkova = {}
        for link in file.links:
            try:
                if mapaSvihMogucihLinkova[link] == link:
                    file.mapForH[link] += 1  # broj linkova u svakom fajlu prema ovom fajlu
                    mapaPotrebnihLinkova[link] = file.mapForH[link]
                    ti = time()
            except Exception:
                0


        for j, key in enumerate(mapaPotrebnihLinkova, start = 0):
            H[j, i] = mapaPotrebnihLinkova[key]/len(mapaPotrebnihLinkova)     #punimo redove od matrice

        for key in mapaSvihMogucihLinkova:
            file.mapaPokazivacaNaFajl[key] = []

        for j, key2 in enumerate(mapaSvihMogucihLinkova, start=0):
            if H[i,j] != 0:
                file.mapaPokazivacaNaFajl[file.name].append(key2)     #dodajem ime u listu

    return H    #napravili smo matricu

def googleRankForFiles(H):
    n = len(H)
    v = np.ones(n)
    v /= n
    v = ((1-d)*v)
    v = np.transpose(v)  # pravimo vektor kolone

    return np.linalg.solve((np.eye(len(H))-d*H),v)     #hopefuly it works , treba da dobijemo vektor sa rangovima fajlova

def rangirajFajlovePoGooglu(parsiraniFajlovi):
    H = findMatrixH(parsiraniFajlovi)
    x = googleRankForFiles(H)
    for i, f in enumerate(parsiraniFajlovi, start = 0):
        f.googleRang = x[i]     #setujemo googlom rang


def RangFiles(searchedFiles, words, globalTrie, parsiraniFajlovi):
    for file in searchedFiles:
        addRangToFile(file, words, globalTrie, parsiraniFajlovi, searchedFiles)

def addRangToFile(file, words, globalTrie, parsiraniFajlovi, searchedFiles):
    brojReciUFajlu = file.numberOfWord  #1. stavka ranga

    vrednostReciUDrugimFajlovima = 0
    for f in searchedFiles:
        if file.file.name in f.file.links:
             vrednostReciUDrugimFajlovima += f.file.googleRang * f.numberOfWord * 10
    
    uticajPokazivaca = 0
    br = 0

    for fajl in file.file.mapaPokazivacaNaFajl:
        br += 1
        f = returnFileByName(parsiraniFajlovi, fajl)

        uticajPokazivaca += f.googleRang *10

    file.file.rang = brojReciUFajlu + uticajPokazivaca + vrednostReciUDrugimFajlovima     #dodeljujemo rang fajlu


def sortFilesByRang(pretrazeniFajlovi):  #algoritam za sortiranje po rangu
    if(len(pretrazeniFajlovi) == 0):
        print("Error")
    sortedFiles = pretrazeniFajlovi
    for i in range(0, len(sortedFiles)):
        for j in range(0, len(sortedFiles)):
            if sortedFiles[j].file.rang > sortedFiles[i].file.rang:
                sortedFiles[i], sortedFiles[j] = sortedFiles[j], sortedFiles[i] #ako je drugi veci menjamo mesta
    return sortedFiles

def returnFileByName(parsiraniFajlovi, fileName):
    for file in parsiraniFajlovi:
        if file.name == fileName:
            return file
    print("File not found")
    return None
