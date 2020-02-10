from parglare import Parser, Grammar
import re
from TrieStruct import GlobalDocumentList

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
    print ("--- Uspesno pretrazen upit ---")
    return subStrings       #ako je provera prosla, znaci da je dobar format


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
        suc, docMap = machingWord(word, globalTrie)
        if suc:     #rec je nadjena
            for key in docMap:
                nalazi = False
                for f in searchedFiles:
                    if key == f.file.name:
                        f.numberOfWord += docMap[key].numberOfWord
                        nalazi = True
                        break
                if not nalazi:
                    searchedFiles.append(docMap[key])

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
                if docList1[file].file.name == docList2[f].file.name:
                    docList1[file].numberOfWord += docList2[f].numberOfWord
                    searchedFiles.append(docList1[file])
                    break

    elif logicalOpp == "OR":
        for file in docList1:
            searchedFiles.append(docList1[file]) # da li je file referenca (orriginal)
        for file in docList2:
            nalazi = False
            for f in searchedFiles:
                if docList2[file].file.name == f.file.name:
                    f.numberOfWord += docList2[file].numberOfWord
                    nalazi = True
                    break
            if not nalazi:
                searchedFiles.append(docList2[file])

    elif logicalOpp == "NOT":
        for file in docList1:
            nalazi = False
            for f in docList2:
                if docList1[file].file.name == docList2[f].file.name:
                    nalazi = True
                    break
            if not nalazi:
                searchedFiles.append(docList1[file])      #ako se pojavljuje u prvom skupu, ne u drugom, dodaj ga

    return searchedFiles

class BinaryTreeNode:
    def __init__(self, data):
        self.pParent = None
        self.pLeft = None
        self.pRight = None
        self.data = data

    def addLeftChild(self, data):
        newNode = BinaryTreeNode(data)
        newNode.pParent = self
        if self.pLeft == None:
            self.pLeft = newNode
        else:
            print("This node already has left child")

    def addRightChild(self, data):
        newNode = BinaryTreeNode(data)
        newNode.pParent = self
        if self.pRight == None:
            self.pRight = newNode
        else:
            print("This node already has right child")

    def isLeaf(self):
        if self.pLeft == None and self.pRight == None:
            return True
        return False


class BinaryTree:
    def __init__(self):
        self.pRoot = None

    def findRoofForNode(self,node):
        while node.pParent != None:
            self.findRoofForNode(node.pParent)
        return node

    def findMostLeftLeafForNode(self, node):
        print(node.data)
        if node.pLeft != None:
            node = self.findMostLeftLeafForNode(node.pLeft)
        return node

    def findRightLeafForNode(self, node):
        pass

    def goOverTree(self):
        currentNode = self.findMostLeftLeafForNode(self.pRoot)    #pocetka tacka obilaska




def complexQuery(queryInput):    #this should return tree
    leftSide = ""
    myTree = BinaryTree()
    lastNode = None
    bracketNode = -1
    nodeAfterBracket = None
    brojOtvorenihZagrada = 0
    while len(queryInput) != 0:
        x = re.search("[a-zA-Z]+|&&|\|\||!|\(|\)", queryInput)      #skeniram string
        if x.group() == None:
            print("Wrong input")

        elif x.group() in("&&", "||"):
            if leftSide == "":
                print("Error, bad entry")
            elif leftSide in("!", "||", "(", "&&"):
                print("Error, bad entry")
            else:           #sve je u redu, dodajemo ga u drvo
                newNode = BinaryTreeNode(x.group())
                if nodeAfterBracket != None:        #znaci da se pojavila zagrada
                    newNode.pLeft = lastNode
                    lastNode.pParent = newNode
                    lastNode = newNode              #sada mi on postaje poslednji
                else:
                    if lastNode.pParent != None:
                        newNode.pParent = lastNode.pParent
                        if lastNode.pParent.pLeft == lastNode:
                            lastNode.pParent.pLeft = newNode
                        else:
                            lastNode.pParent.pRight = newNode
                    lastNode.pParent = newNode
                    newNode.pLeft = lastNode
                    myTree.pRoot = newNode
                    lastNode = newNode      #nakon sto smo ubacili node, lastNode postaje taj poslednje ubaceni cvor

        elif x.group() == "(":
            if leftSide not in("", "&&", "!", "||", "("):
                print("Error, bad entry")
            else:       #potrebno je povecati broj otvorenih zagrada
                if myTree.pRoot == None:
                    bracketNode = None
                    lastNode = myTree.pRoot
                else:
                    bracketNode = lastNode  #bracket node mi je && ili || na koji posle treba da se uvece podstablo
                brojOtvorenihZagrada += 1

        elif x.group() == ")":
            if leftSide == "":
                print("Error, bad entry")
            elif leftSide in("(", "&&", "||", "!"):
                print("Error, bad entry")
            else:
                brojOtvorenihZagrada -= 1
                if brojOtvorenihZagrada == 0:   #ovo je znak da traba da uvezemo podstablo u stablo
                    roofNode = myTree.findRoofForNode(nodeAfterBracket)
                    if bracketNode == None:   #znaci da jos nista nema u stablu
                        myTree.pRoot = roofNode     #roof postaje koren
                    else:
                        bracketNode.pRight = roofNode
                        roofNode.pParent = bracketNode
                    nodeAfterBracket = None         #sada smo uvezali podstablo u stablo
                    lastNode = myTree.pRoot
                else:
                    lastNode = myTree.findRoofForNode(lastNode)     #sada opeerator u zagradi postaje last node posto imamo jos jednu zagradu

        elif x.group() == "!":

            if leftSide not in("", "(", "&&", "||"):
                print("Error, bad entry")
            else:
                newNode = BinaryTreeNode(x.group())
                if myTree.pRoot == None and leftSide != "(":
                    myTree.pRoot = newNode
                    lastNode = myTree.pRoot
                else:
                    if leftSide == "(" and nodeAfterBracket == None:
                        nodeAfterBracket = newNode
                    else:   #ispred su ili && ili ||,   uvezujemo ga
                        lastNode.pRight = newNode
                        newNode.pParent = lastNode
                    lastNode = newNode

        else:       #nasli smo rec
            newNode = BinaryTreeNode(x.group())
            if myTree.pRoot == None and leftSide != "(":
                myTree.pRoot = newNode
                lastNode = myTree.pRoot
            else:
                if leftSide in("&&", "||"):
                    lastNode.pRight = newNode
                    newNode.pParent = lastNode
                elif leftSide == "(" and nodeAfterBracket == None:
                    nodeAfterBracket = newNode
                elif leftSide == "!":
                    lastNode.pLeft = newNode
                    newNode.pParent = lastNode
                lastNode = newNode

        leftSide = x.group()
        queryInput = queryInput[x.end():]


    if leftSide in ("&&", "!", "||", "("):
        print("Error, bad entry")       #neuspesno parsiranje

    return myTree

def complexSearch(myTree, node2, globalTree, parsedSet):
    node = myTree.findMostLeftLeafForNode(node2)  # pocetni cvor
    sucLeft, leftDocuments = machingWord(node.data, globalTree)  # skup dokumenata iz mape
    rightDocuments = None
    returnSkup = []
    opp = node.pParent
    if opp == None:
        return leftDocuments
    if opp.data == "!":
        fileSet = set()
        for doc in leftDocuments:
            fileSet.add(leftDocuments[doc].file)
        fileSet = parsedSet - fileSet
        leftDocuments = []
        for f in fileSet:
            newDoc = GlobalDocumentList(f)
            newDoc.numberOfWord = 0
            leftDocuments.append(newDoc)
        return leftDocuments
    else:
        if not opp.pRight.isLeaf():
            print("Rekurzivni poziv")
            leftDocuments = complexSearch(myTree, opp.pRight, globalTree, parsedSet)
        sucRight, rightDocuments = machingWord(opp.pRight.data, globalTree)
        if opp.data == "&&":
            for file in leftDocuments:
                for f in rightDocuments:
                    if leftDocuments[file].file.name == rightDocuments[f].file.name:
                        leftDocuments[file].numberOfWord += rightDocuments[f].numberOfWord
                        returnSkup.append(leftDocuments[file])
                        break
        else:   #||
            for file in leftDocuments:
                returnSkup.append(leftDocuments[file])  # da li je file referenca (orriginal)
            for file in rightDocuments:
                nalazi = False
                for f in returnSkup:
                    if rightDocuments[file].file.name == f.file.name:
                        f.numberOfWord += rightDocuments[file].numberOfWord
                        nalazi = True
                        break
                if not nalazi:
                    returnSkup.append(rightDocuments[file])
        return returnSkup