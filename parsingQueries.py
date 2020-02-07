from parglare import Parser, Grammar

def simpleQuery(userInput):     #u prostom upitu treba uneti reci razdvojene razmakom, nema puno filozofije
    subStrings = userInput.split(' ')
    return subStrings

LogicalOpps = ["AND", "OR", "NOT"]

def logicalQuery(userInput):
    subStrings = userInput.split(' ')
    if len(subStrings) != 3:
        print("Error, not a good format")
        return None
    if (subStrings[0] in LogicalOpps) or (subStrings[-1] in LogicalOpps) or (subStrings[1] not in LogicalOpps):
        print("Error, not a good format")
        return None
    return subStrings       #ako je provera prosla, znaci da je dobar format

def complexQuery(queryInput):    #this should return tree
    # grammar = r"""
    #
    # query
    # : subQuery
    # | query opp_type subQuery
    # ;
    #
    # subQuery
    # : _WORD
    # | _WORD opp_type _WORD
    # | _NOT _LPAREN subQuery _RPAREN
    # ;
    #
    # opp_type
    # : _AND
    # | _OR
    # ;
    #
    # terminals
    # _NOT: "!";
    # _AND: "&&";
    # _OR: "||";
    # _LPAREN: "(";
    # _RPAREN: ")";
    # _WORD: /[a-zA-Z]+/
    # """
    g1 = """
        S: "2" b? "3"?;
        
        terminals
        b: "1";
    """
    g = Grammar.from_string(g1)
    p = Parser(g, build_tree=True)
    res = p.parse(queryInput)
    # parser = Parser(grammar)
    # result = parser.parse(queryInput, build_tree=True)
    return res

def findLeaf(tree, node):
    if len(node.children) != 0:
        newnode = node.children[0]
        findLeaf(tree, newnode)
    return node

# if __name__ == "__main__":
#     input = input("Query: ")
#     tree = complexQuery(input)
#     print(tree.tree_str())


def machingWord(word, globalTrie):
    pCurrent = globalTrie.root
    for c in word:
        pOld = pCurrent
        for child in pCurrent.children:
            if c == child.data:
                pCurrent = child
                break
        if pOld == pCurrent:
            return (False, None)
    return (True, pCurrent.documents)       #vracamo listu fajlova koji sadrze tu rec, kao i broj reci u tom fajlu


def simpleSearch(words, globalTrie):
    searchedFiles = []    #sadrzi fajlove i ukupan broj trazenih reci koje sadrze ti fajlovi, treba nam zbog rangiranja
    for word in words:
        suc, docList = machingWord(word, globalTrie)
        if suc:     #rec je nadjena
            for file in docList:
                nalazi = False
                for f in searchedFiles:
                    if file.file.name == f.file.name:
                        f.numberOfWord += file.numberOfWord
                        nalazi = True
                        break
                if not nalazi:
                    searchedFiles.append(file)

    return searchedFiles

def logicalSearch(words, globalTrie):
    firstWord = words[0]
    logicalOpp = words[1]
    secondWord = words[-1]

    suc1, docList1 = machingWord(firstWord, globalTrie)     #ovde ce mi biti lista fajlova koji sadrze prvu rec
    suc2, docList2 = machingWord(secondWord, globalTrie)    #ovde mi je lista fajlova koji sadrze drugu rec

    searchedFiles = []

    if logicalOpp == "AND":
        for file in docList1:
            for f in docList2:
                if file.file.name == f.file.name:
                    print(file.file.name, " ", file.numberOfWord, " ", f.numberOfWord)
                    file.numberOfWord += f.numberOfWord
                    searchedFiles.append(file)
                    break

    elif logicalOpp == "OR":
        for file in docList1:
            searchedFiles.append(file) # da li je file referenca (orriginal)
        for file in docList2:
            nalazi = False
            for f in searchedFiles:
                if file.file.name == f.file.name:
                    f.numberOfWord += file.numberOfWord
                    nalazi = True
                    break
            if not nalazi:
                searchedFiles.append(file)

    elif logicalOpp == "NOT":
        for file in docList1:
            nalazi = False
            for f in docList2:
                if file.file.name == f.file.name:
                    nalazi = True
                    break
            if not nalazi:
                searchedFiles.append(file)      #ako se pojavljuje u prvom skupu, ne u drugom, dodaj ga

    return searchedFiles

