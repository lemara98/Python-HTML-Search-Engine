from parser import Parser
import os
from parsingFiles import parseFiles
from TrieStruct import GlobalTrie
def menu():
    print("1. parse files")
    print("2. enter the query")
    print("3. search documents")
    print("4. print result")
    print("5. pagination")
    print()
    userInput = input("choose option")
    return userInput


def main():
    query = ""  #query za search
    p = Parser()
    abs_path = os.path.abspath(os.getcwd())  #inicijalizujemo path na crnt working dir
    parsiraniFajlovi = []  # ovde cuvamo isparsirane fajlove
    pretrazeniFajlovi = []
    userInput = 1
    globalTrie = None
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
            globalTrie = GlobalTrie(parsiraniFajlovi)   #ovde se pravi globalno drvo
            print("///////////////////////////////////////")
            for file in parsiraniFajlovi:
                print(file.name)

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
                    badEntry = False
                elif queryInput == "2":
                    badEntry = False
                elif queryInput == "3":
                    badEntry = False
                else:
                    print("You didn't choose correctly, please choose again")

        elif userInput == "3":
            badEntry = True
            while badEntry:
                print("1. basic search")
                print("2. rang search")
                searchInput = input("choose option")
                if searchInput == "1":
                    badEntry = False
                elif searchInput == "2":
                    badEntry = False
                else:
                    print("You didn't choose correctly, please choose again")

        elif userInput == "4":
            for file in pretrazeniFajlovi:
                # file.printParseResult()
                print(file.name, " ", file.rang)

        elif userInput == "5":
            pass

if __name__ == "__main__":
    main()