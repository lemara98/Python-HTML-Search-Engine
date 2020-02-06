from parser import Parser
import os
from parsingFiles import parseFiles
from TrieStruct import GlobalTrie
import parsingQueries
from time import time
from rangFiles import rangirajFajlovePoGooglu
from rangFiles import RangFiles, sortFilesByRang
from pagination import PaginatePages
def menu():
    print("1. Parse files")
    print("2. Enter the query")
    print("3. Rang files")
    print("4. Print result")
    print("5. Pagination")
    print("0. Exit")
    print()
    userInput = input("Choose option: ")
    return userInput


def main():
    p = Parser()
    abs_path = os.path.abspath(os.getcwd())  #inicijalizujemo path na crnt working dir
    parsiraniFajlovi = []  # ovde cuvamo isparsirane fajlove
    searchedFiles = []
    sortedFiles = []
    userInput = 1
    globalTrie = None
    queryWords = None
    queryInput = 0
    searchInput = 0
    while userInput != 0:
        userInput = menu()

        if userInput == "1":
            if len(parsiraniFajlovi) != 0:
                print("Files already parsed")
                continue
            rel_path = input("Izaberite root direktorijum, relativnu putanju od 'Drudi projektni zadatak': ")
            abs_path = os.path.abspath(os.path.dirname(rel_path))
            parseFiles(abs_path, p, parsiraniFajlovi)
            rangirajFajlovePoGooglu(parsiraniFajlovi)   #dodeljujemo googlov rang fajlovima
            t0 = time()
            globalTrie = GlobalTrie(parsiraniFajlovi)   #ovde se pravi globalno drvo
            tn = time()
            print(tn-t0)
            print("///////////////////////////////////////")
            for file in parsiraniFajlovi:
                print(file.name)
            print("///////////trie////////////")
            globalTrie.printTrie(globalTrie.root)


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
                    query = input("Enter query: ")
                    words = parsingQueries.simpleQuery(query)
                    queryWords = words
                    searchedFiles = parsingQueries.simpleSearch(words, globalTrie)
                    badEntry = False
                elif queryInput == "2":
                    query = input("Enter query: ")
                    words = parsingQueries.logicalQuery(query)
                    queryWords = words
                    searchedFiles = parsingQueries.logicalSearch(words, globalTrie)
                    badEntry = False
                elif queryInput == "3":
                    badEntry = False
                else:
                    print("You didn't choose correctly, please choose again")

        elif userInput == "3":
            RangFiles(searchedFiles, queryWords, globalTrie)
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
                    for file in sortedFiles:
                        print(file.file.name, file.file.rang)
                    badEntry = False

                else:
                    print("You didn't choose correctly, please choose again")

        elif userInput == "5":
            N = input("Number of files on one page: ")
            PaginatePages(searchedFiles, N) # Mozda bismo trebali rangirane fajlove!

        elif userInput == "0":
            break



if __name__ == "__main__":
    main()