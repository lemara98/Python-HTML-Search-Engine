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
    print("*********************")
    print("\tSadrzaj")
    print("1. Parse files")
    print("2. Enter the query")
    print("3. Rang files")
    print("4. Print result")
    print("5. Pagination")
    print("6. Graf rezultata")
    print("0. Exit")
    print ("*********************")
    print()
    userInput = input("Choose option: ")
    return userInput


def main():
    p = Parser()
    G = GraphResult()
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
            parsiraniFajlovi = []
            abs_path = os.path.abspath (os.getcwd ())  # inicijalizujemo path na crnt working dir
            # if len(parsiraniFajlovi) != 0:
            #     print("Files already parsed")
            #     continue
            print("Za izlaz iz opcije unesite 0")
            rel_path = input("Unesite 0 ili root direktorijum, relativnu putanju od '" + abs_path + "': ")
            if rel_path == '0':
                continue

            abs_path = os.path.join(abs_path,rel_path)
            if not os.path.exists(abs_path):
                print("Ne postoji takav direktorijum!")
                continue
            print("--- Vrsi se parsiranje unetog korenskog direktorijuma ---")
            t0 = time ()
            parseFiles(abs_path, "", p, parsiraniFajlovi)
            t1 = time()
            print("--- Parsiranje unetog korenskog direktorijuma zavrseno ---")
            print("--- Vrsi se dodela google ranga svim parsiranim fajlovima (.html) ---")
            rangirajFajlovePoGooglu(parsiraniFajlovi)   #dodeljujemo googlov rang fajlovima
            t2 = time()
            print("--- Zavrseno dodeljivanje google ranga fajlovima ---")
            print("--- Vrsi se unos u globalno Trie stablo ---")
            globalTrie = GlobalTrie(parsiraniFajlovi)
            t3 = time()
            print("--- Globalno Trie stablo je napravljeno ---")
            tn = time ()
            print("***************************************************************************")
            print("\t\tVREMENA UTROSENA ZA RADNJE")
            print("Vreme parsiranja: ", t1 - t0)
            print("Vreme za gugl rangiranje: ", t2 - t1)
            print("Vreme za pravljenje stabla: ", t3 - t2)
            print("Ukupno vreme potrebno za parsiranje i kreiranej stabla: ", tn - t0)
            print("broj parsiranih fajlova: ", len(parsiraniFajlovi))
            print("***************************************************************************")


        elif userInput == "2":
            if len (parsiraniFajlovi) == 0:
                print("Prvo isparsirati fajlove")
                continue
            badEntry = True
            while badEntry:
                print("Query types: ")
                print("1. Simple query (word1 word2 ... wordn), n = 1,2,3,...")
                print("2. Logical query (word1 LOPP word2), LOPP = {AND, OR, NOT}")
                print("3. Complex query (word1 COPP word2 COPP word3 ...), COPP = {!, &&, ||}, example: (!bird && !git) || python")
                print("0. Za izlaz iz opcije")
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
                    print ("--- Uspesno pretrazene reci ---")
                elif queryInput == "2":
                    searchQueryChoosen = 2
                    query = input("Enter query: ")
                    words = parsingQueries.logicalQuery(query)
                    queryWords = words
                    if words is not None:
                        searchedFiles = parsingQueries.logicalSearch(words, globalTrie)
                    badEntry = False
                elif queryInput == "3":
                    query = input("Enter query: ")
                    myTree = parsingQueries.complexQuery(query)
                    set1 = set(parsiraniFajlovi)
                    searchedFiles = parsingQueries.complexSearch(myTree, myTree.pRoot, globalTrie, set1)
                 #  words = parsingQueries.complexQuery()
                    searchQueryChoosen = 3
                    badEntry = False
                    print("--- Uspesno pretrazen kompleksan upit ---") # u kompleks query!!!!!
                elif queryInput == '0':
                    break
                else:
                    print("You didn't choose correctly, please choose again")


        elif userInput == "3":
            if len(parsiraniFajlovi) == 0:
                print("Prvo parsirati fajlove")
            if len (searchedFiles) == 0:
                print("Skup pretrazenih fajlova je prazan!")
                print("Uraditi pretragu")
                continue
            RangFiles(searchedFiles, queryWords, globalTrie, parsiraniFajlovi)
            sortedFiles = sortFilesByRang(searchedFiles)
            print("--- Uspesno rangirani fajlovi ---")

        elif userInput == "4":
            badEntry = True
            while badEntry:
                print("1. Basic print")
                print("2. Rang print")
                print("0. Izlaz iz opcije")
                searchInput = input("choose option")
                if searchInput == "1":
                    for file in searchedFiles:
                        print(file.file.name)
                    badEntry = False
                elif searchInput == "2":
                    l = len(sortedFiles)
                    for file in sortedFiles:
                        print(l, ")", file.file.name, file.file.rang, file.numberOfWord)
                        l-=1
                    badEntry = False
                elif searchInput == '0':
                    break
                else:
                    print("You didn't choose correctly, please choose again")
            print("--- Uspesno izvrsen ispis ---")

        elif userInput == "5":
            print("Za izlaz iz opcije - bilo sta nelogicno")
            N = input("Number of files on one page: ")  # NE radi dobro za poslednju stranicu!!!!!!!!!!!
            PaginatePages(searchedFiles, N) # Mozda bismo trebali rangirane fajlove!


        elif userInput == "6":
            G1 = GraphResult()
            fileNames = []      # ime fajlova koji sadrze trazenu rec
            # if searchQueryChoosen == 1:
            #     for word in queryWords: #google, OR, Google
            #         suc, docList = machingWord (word, globalTrie)
            #         for file in docList:
            #             fileNames.append(docList[file].file.name)    #stavlja imena fajlova u listu
            # elif searchQueryChoosen == 2:
            #     suc1,docList1 = machingWord(queryWords[0], globalTrie)
            #     suc2,docList2 = machingWord(queryWords[-1], globalTrie)
            #     for file in docList1:
            #         fileNames.append(docList1[file].file.name)
            #     for file in docList2:
            #         fileNames.append(docList2[file].file.name)
            # elif searchQueryChoosen == 3:
            for file in sortedFiles:
                fileNames.append(file.file.name)
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