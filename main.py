from locale import atoi

from parser1 import Parser
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
    print("\tContent")
    print("1. Parse files")
    print("2. Enter the query")
    print("3. Rang files")
    print("4. Print result")
    print("5. Pagination")
    print("6. Graph")
    print("0. Exit")
    print("*********************")
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
    rangirano = False
    searchQueryChoosen = 0
    while userInput != 0:
        userInput = menu()

        if userInput == "1":
            parsiraniFajlovi = []
            rangirano = False
            abs_path = os.path.abspath(os.getcwd())  # inicijalizujemo path na crnt working dir
            # if len(parsiraniFajlovi) != 0:
            #     print("Files already parsed")
            #     continue
            # print("Za izlaz iz opcije unesite 0")
            print("0. Exit")
            # rel_path = input("Unesite 0 ili root direktorijum, relativnu putanju od '" + abs_path + "': ")
            rel_path = input(
                "For parse enter root directory, relative path from '" + abs_path + "' (recommended: test-skup): ")
            if rel_path == '0':
                continue

            abs_path = os.path.join(abs_path, rel_path)
            if not os.path.exists(abs_path):
                # print("Ne postoji takav direktorijum!")
                print("This directory doesn't exist")
                continue
            # print("--- Vrsi se parsiranje unetog korenskog direktorijuma ---")
            print("--- Parsing files from entered root directory ---")
            t0 = time()
            parseFiles(abs_path, "", p, parsiraniFajlovi)
            t1 = time()
            # print("--- Parsiranje unetog korenskog direktorijuma zavrseno ---")
            print("--- Finished parsing - FINISHED ---")
            # print("--- Vrsi se dodela google ranga svim parsiranim fajlovima (.html) ---")
            print("--- Ranging all parsed files (.html) ---")
            rangirajFajlovePoGooglu(parsiraniFajlovi)  # dodeljujemo googlov rang fajlovima
            t2 = time()
            # print("--- Zavrseno dodeljivanje google ranga fajlovima ---")
            print("--- Ranging all parsed files - FINISHED ---")
            # print("--- Vrsi se unos u globalno Trie stablo ---")
            print("--- Forming global trie tree structure ---")
            globalTrie = GlobalTrie(parsiraniFajlovi)
            t3 = time()
            # print("--- Globalno Trie stablo je napravljeno ---")
            print("--- Forming global trie tree structure - FINISHED ---")
            tn = time()
            print("***************************************************************************")
            # print("\t\tVREMENA UTROSENA ZA RADNJE")
            print("\t\tTIME STATISTICS")
            # print("Vreme parsiranja: ", t1 - t0)
            print("Parsing time: ", t1 - t0)
            # print("Vreme za gugl rangiranje: ", t2 - t1)
            print("Ranging time: ", t2 - t1)
            # print("Vreme za pravljenje stabla: ", t3 - t2)
            print("Global trie tree forming time: ", t3 - t2)
            # print("Ukupno vreme potrebno za parsiranje i kreiranej stabla: ", tn - t0)
            print("Total time: ", tn - t0)
            # print("broj parsiranih fajlova: ", len(parsiraniFajlovi))
            print("Number of parsed files: ", len(parsiraniFajlovi))
            print("***************************************************************************")


        elif userInput == "2":
            if len(parsiraniFajlovi) == 0:
                # print("Prvo isparsirati fajlove")
                print("First you need to parse files!")
                continue
            badEntry = True
            while badEntry:
                print("Query types: ")
                print("1. Simple query (word1 word2 ... wordn), n = 1,2,3,...")
                print("2. Logical query (word1 LOPP word2), LOPP = {AND, OR, NOT}")
                print(
                    "3. Complex query (word1 COPP word2 COPP word3 ...), COPP = {!, &&, ||}, example: (!bird && !git) || python")
                print("0. exit")
                # print("choose option")
                queryInput = input("Choose option: ")
                if queryInput == "1":
                    searchQueryChoosen = 1
                    query = input("Enter query: ")
                    words = parsingQueries.simpleQuery(query)
                    queryWords = words
                    if words is not None:
                        searchedFiles = parsingQueries.simpleSearch(words, globalTrie)
                    badEntry = False
                    rangirano = False
                    # print ("--- Uspesno pretrazene reci ---")
                    print("--- Successfully searched word(s) ---")
                elif queryInput == "2":
                    searchQueryChoosen = 2
                    query = input("Enter query: ")
                    words = parsingQueries.logicalQuery(query)
                    queryWords = words
                    if words is not None:
                        searchedFiles = parsingQueries.logicalSearch(words, globalTrie)
                    badEntry = False
                    rangirano = False
                elif queryInput == "3":
                    query = input("Enter query: ")
                    myTree = parsingQueries.complexQuery(query)
                    set1 = set(parsiraniFajlovi)
                    searchedFiles = parsingQueries.complexSearch(myTree, myTree.pRoot, globalTrie, set1)
                    #  words = parsingQueries.complexQuery()
                    searchQueryChoosen = 3
                    badEntry = False
                    rangirano = False
                    # print("--- Uspesno pretrazen kompleksan upit ---") # u kompleks query!!!!!
                    print("--- Successfully searched complex query ---")
                elif queryInput == '0':
                    break
                else:
                    print("You didn't choose correctly, please choose again")


        elif userInput == "3":
            if len(parsiraniFajlovi) == 0:
                # print("Prvo parsirati fajlove")
                print("First you need to parse files!")
                continue
            if len(searchedFiles) == 0:
                # print("Skup pretrazenih fajlova je prazan!")
                print("Searched set of files is empty!")
                # print("Uraditi pretragu")
                print("Do search")
                continue
            RangFiles(searchedFiles, queryWords, globalTrie, parsiraniFajlovi)
            sortedFiles = sortFilesByRang(searchedFiles)
            rangirano = True
            # print("--- Uspesno rangirani fajlovi ---")
            print("--- Successfully ranged files ---")

        elif userInput == "4":
            if len(parsiraniFajlovi) == 0:
                # print("Prvo parsirati fajlove")
                print("First you need to parse files!")
                continue
            if len(searchedFiles) == 0:
                # print("Skup pretrazenih fajlova je prazan!")
                print("Searched set of files is empty!")
                # print("Uraditi pretragu")
                print("Do search")
                continue
            badEntry = True
            while badEntry:
                print("1. Basic print")
                print("2. Rang print")
                print("0. Exit")
                searchInput = input("Choose option: ")
                if searchInput == "1":
                    for file in searchedFiles:
                        print(file.file.name)
                    badEntry = False
                elif searchInput == "2":
                    l = len(sortedFiles)
                    print("\t\tDocument Name\t|\tTotal Score\t|\t Number of query matches in doc.")
                    for file in sortedFiles:
                        print(l, ") ", file.file.name, file.file.rang, file.numberOfWord)
                        l -= 1
                    badEntry = False
                elif searchInput == '0':
                    break
                else:
                    print("You didn't choose correctly, please choose again")
            # print("--- Uspesno izvrsen ispis ---")
            print("--- Successful output ---")

        elif userInput == "5":
            if len(parsiraniFajlovi) == 0:
                # print ("Prvo parsirati fajlove")
                print("First you need to parse files!")
                continue
            if len(searchedFiles) == 0:
                # print("Skup pretrazenih fajlova je prazan!")
                print("Searched set of files is empty!")
                # print("Uraditi pretragu")
                print("Do search")
                continue
            while True:
                print("0. Exit")
                N = input("Number of files on one page: ")  # NE radi dobro za poslednju stranicu!!!!!!!!!!!
                if N.isdigit():
                    N = atoi(N)
                    if N > 0:
                        PaginatePages(searchedFiles, N)  # Mozda bismo trebali rangirane fajlove!
                        break
                    else:
                        break
                else:
                    break


        elif userInput == "6":
            if len(parsiraniFajlovi) == 0:
                # print("Prvo parsirati fajlove")
                print("First you need to parse files!")
                continue
            if len(searchedFiles) == 0:
                # print("Skup pretrazenih fajlova je prazan!")
                print("Searched set of files is empty!")
                # print("Uraditi pretragu")
                print("Do search")
                continue
            if rangirano == False:
                # print("Rangirajte da biste videli graf")
                print("Rang files first in order to see the result graph")
                continue
            G1 = GraphResult()
            fileNames = []  # ime fajlova koji sadrze trazenu rec
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
    print("\n----------------------------------------\n")
    print("Welcome to python HTML Search engine")
    print("Developed by: hadzija7 & lemara98")
    print("\n----------------------------------------\n")
    main()
