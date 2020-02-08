from parser import Parser
import os
from parsingFiles import parseFiles
from TrieStruct import GlobalTrie
import parsingQueries
from time import time
from rangFiles import rangirajFajlovePoGooglu
from rangFiles import RangFiles, sortFilesByRang
from pagination import PaginatePages
from GraphStruct import GraphResult
from parsingQueries import machingWord
def menu():
    print("1. Parse files")
    print("2. Enter the query")
    print("3. Rang files")
    print("4. Print result")
    print("5. Pagination")
    print("6. Graf rezultata")
    print("0. Exit")
    print()
    userInput = input("Choose option: ")
    return userInput


def main():
    p = Parser()
    G = GraphResult()
    abs_path = os.path.abspath(os.getcwd())  #inicijalizujemo path na crnt working dir
    parsiraniFajlovi = []  # ovde cuvamo isparsirane fajlove
    searchedFiles = []
    sortedFiles = []
    userInput = 1
    globalTrie = None
    queryWords = None
    queryInput = 0
    searchInput = 0
    searchQueryChoosen = 0
    while userInput != 0:
        userInput = menu()

        if userInput == "1":
            if len(parsiraniFajlovi) != 0:
                print("Files already parsed")
                continue
            rel_path = input("Izaberite root direktorijum, relativnu putanju od 'Drudi projektni zadatak': ")
            t0 = time ()
            abs_path = os.path.join(abs_path,rel_path)
            parseFiles(abs_path, "", p, parsiraniFajlovi)
            t1 = time()
            #G.prikazi_graficki_rezultat()

            rangirajFajlovePoGooglu(parsiraniFajlovi)   #dodeljujemo googlov rang fajlovima
            t2 = time()
            globalTrie = GlobalTrie(parsiraniFajlovi)
            t3 = time()


            for file in parsiraniFajlovi:
                print(file.name)
            print("///////////trie////////////")
            globalTrie.printTrie(globalTrie.root)
            tn = time ()
            print("Vreme parsiranja: ", t1 - t0)
            print("Vreme za gugl rangiranje: ", t2 - t1)
            print("Vreme za pravljenje stabla: ", t3 - t2)
            print("Vreme za stampanje drveta: ", tn - t3)
            print ("Ukupno vreme potrebno za parsiranje i kreiranej stabla: ", tn - t0)
            print("broj parsiranih fajlova: ", len(parsiraniFajlovi))


        elif userInput == "2":
            badEntry = True
            while badEntry:
                print("query types: ")
                print("1. simple query (word1 word2 ... wordn), n = 1,2,3,...")
                print("2. logical query (word1 LOPP word2), LOPP = {AND, OR, NOT}")
                print("3. complex query (word1 COPP word2 COPP word3 ...), COPP = {!, &&, ||}, example: (!bird && !git) || python")
                print("choose option")
                queryInput = input()
                if queryInput == "1":
                    searchQueryChoosen = 1
                    query = input("Enter query: ")
                    words = parsingQueries.simpleQuery(query)
                    queryWords = words
                    if words is not None:
                        searchedFiles = parsingQueries.simpleSearch(words, globalTrie)
                    badEntry = False
                elif queryInput == "2":
                    searchQueryChoosen = 2
                    query = input("Enter query: ")
                    words = parsingQueries.logicalQuery(query)
                    queryWords = words
                    if words is not None:
                        searchedFiles = parsingQueries.logicalSearch(words, globalTrie)
                    badEntry = False
                elif queryInput == "3":
                    searchQueryChoosen = 3
                    badEntry = False
                else:
                    print("You didn't choose correctly, please choose again")

        elif userInput == "3":
            RangFiles(searchedFiles, queryWords, globalTrie, parsiraniFajlovi)
            sortedFiles = sortFilesByRang(searchedFiles)

        elif userInput == "4":
            badEntry = True
            while badEntry:
                print("1. basic print")
                print("2. rang print")
                searchInput = input("choose option")
                if searchInput == "1":
                    for file in searchedFiles:
                        print(file.file.name, file.file.googleRang)
                    badEntry = False
                elif searchInput == "2":
                    l = len(sortedFiles)
                    for file in sortedFiles:
                        print(l, ")", file.file.name, file.file.rang, file.numberOfWord)
                        l-=1
                    badEntry = False

                else:
                    print("You didn't choose correctly, please choose again")

        elif userInput == "5":
            N = input("Number of files on one page: ")  # NE radi dobro za poslednju stranicu!!!!!!!!!!!
            PaginatePages(searchedFiles, N) # Mozda bismo trebali rangirane fajlove!

        elif userInput == "6":
            G1 = GraphResult()
            fileNames = []      # ime fajlova koji sadrze trazenu rec
            if searchQueryChoosen == 1:
                for word in queryWords: #google, OR, Google
                    suc, docList = machingWord (word, globalTrie)
                    for file in docList:
                        fileNames.append(file.file.name)    #stavlja imena fajlova u listu
            elif searchQueryChoosen == 2:
                suc1,docList1 = machingWord(queryWords[0], globalTrie)
                suc2,docList2 = machingWord(queryWords[-1], globalTrie)
                for file in docList1:
                    fileNames.append(file.file.name)
                for file in docList2:
                    fileNames.append(file.file.name)
            elif searchQueryChoosen == 3:
                pass        #za komplex query

            for file in sortedFiles:
                linksForGraph = []  # lista linkova za graf koji pokazuju na fajlove koji sadrze trazenu rec ->fileNames
                for link in file.file.links:
                    if link in fileNames:
                        linksForGraph.append(link)
                G1.dodajCvorUGraf(file.file.name, linksForGraph, file.file.rang)
            G1.prikazi_graficki_rezultat()
            # PROVERITI DA LI GRAF SA LINKOVIMA VALJA U ODNOSU NA TESTOVE PRE UNETIH SADASNJIH IZMENA!!!!

        elif userInput == "0":
            break



if __name__ == "__main__":
    main()