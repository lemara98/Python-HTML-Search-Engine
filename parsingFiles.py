
import os
from GraphStruct import GraphResult

class ParseResult:
    def __init__(self, links, words, name):
        self.links = links
        self.words = words
        self.name = name
        self.googleRang = 0
        self.mapForH = {}  # this is map/dict for matrixH (google rank)
        for link in self.links:
            self.mapForH[os.path.basename(link)] = 0  # inicijalizujemo recnik
        self.rang = 0


# def parseFiles(abs_path, nb, parser, parsiraniFilovi):
#     for filename in os.listdir(abs_path):
#         print(filename)
#         directory_path = os.path.join(abs_path, filename)
#
#         if os.path.isdir(directory_path):  #ako je datoteka onda se rekurzivno poziva funkcija
#             parseFiles(directory_path,nb,parser,parsiraniFilovi)
#         elif filename.endswith("html"):
#             s = tuple(parser.parse(directory_path))
#             pp = ParseResult(s[0], s[-1], filename)
#             pp.absolutePath = directory_path    #absolutna putanja do fajla
#             parsiraniFilovi.append(pp)

#   abs_path    -   najduza zajednicka putanja
#   rel_path    -   zasebna putanja od abs_path-a
#   parser      -   parser
#   parsiraniFajlovi -  skup obradjenih .html fajlova

def parseFiles(abs_path, rel_path, parser, parsiraniFilovi):
    for filename in os.listdir(os.path.join(abs_path, rel_path)):
        print(len(os.listdir(os.path.join(abs_path, rel_path))))
        if len(os.listdir(os.path.join(abs_path, rel_path))) == 1:
            director = os.path.join(os.path.join(abs_path, rel_path), filename)
            if os.path.isdir(director) and len(parsiraniFilovi) == 0 :
                abs_path = director
                parseFiles(abs_path, rel_path, parser, parsiraniFilovi)
                break


        print(rel_path)
        directory_path = os.path.join(abs_path, rel_path)
        directory_path = os.path.join (directory_path, filename)
        if os.path.isdir(directory_path):  #ako je datoteka onda se rekurzivno poziva funkcija
            temp = rel_path
            rel_path = os.path.join(rel_path, filename)
            parseFiles(abs_path, rel_path, parser, parsiraniFilovi)
            rel_path = temp
        elif filename.endswith("html"):
            s = tuple(parser.parse(directory_path))
            putanja = os.path.join(rel_path, filename)
            pp = ParseResult(s[0], s[-1], putanja)
            for i in range(len(pp.links)):
                print("/////")
                print(pp.links[i])
                pp.links[i] = os.path.relpath(pp.links[i], abs_path)
                print(pp.links[i])
            parsiraniFilovi.append(pp)