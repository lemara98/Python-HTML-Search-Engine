

class GlobalDocumentList:
    def __init__(self, parsedFile):
        self.file = parsedFile      #this is our document
        self.numberOfWord = 1

class GlobalTrieNode:
    def __init__(self, data):
        self.parent = None
        self.children = []      #lista slova sortirana po alfabetu
        self.data = data    #karakter
        self.documents = []     #treba napraviti strukturu, videti sta nam sve treba ovde

    def addChild(self, node):
        for i, child in enumerate(self.children, start = 0):
            if node.data < child.data:
                self.children.insert(i,node)
                return
        self.children.append(node)

    def hasChildren(self):
        return self.children is not None


class GlobalTrie:
    def __init__(self, parsiraniFajlovi):
        self.root = GlobalTrieNode("root")
        pCurrentNode = None
        for file in parsiraniFajlovi:
            for word in file.words:
                pCurrentNode = self.root
                for i, c in enumerate(word, start=0):
                    if not pCurrentNode.hasChildren():  # ako nema deca dodaj
                        newNode = GlobalTrieNode(c)
                        pCurrentNode.addChild(newNode)
                        pCurrentNode = newNode  # da li sada pokazuje na stvarnog sina ?
                    else:
                        oldCurrentNode = pCurrentNode
                        for child in pCurrentNode.children:
                            if child.data == c:  # pronasao je slovo(vec postoji)
                                pCurrentNode = child
                                break
                        if oldCurrentNode == pCurrentNode:
                            newNode = GlobalTrieNode(c)
                            pCurrentNode.addChild(newNode)
                            pCurrentNode = newNode

                    #ako smo dosli do kraja reci, sada treba upisati dokument(file) koji sadrzi tu rec u listu fajlova u tom cvoru, takodje broj reci u tom fajlu
                    postoji = False
                    if i == (len(word) - 1):
                        index = 0
                        for j, doc in enumerate(pCurrentNode.documents, start = 0):
                            if doc.file.name == file.name:
                                postoji = True
                                index = j
                                break
                        if not postoji:
                            newDoc = GlobalDocumentList(file)
                            pCurrentNode.documents.append(newDoc)
                        else:
                            pCurrentNode.documents[index].numberOfWord += 1     #povecavamo broj reci u tom dokumentu