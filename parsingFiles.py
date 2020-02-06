
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


def parseFiles(abs_path, parser, parsiraniFilovi, G):
    for filename in os.listdir(abs_path):
        print(filename)
        directory_path = os.path.join(abs_path, filename)

        if os.path.isdir(directory_path):  #ako je datoteka onda se rekurzivno poziva funkcija
            parseFiles(directory_path,parser,parsiraniFilovi, G)
        elif filename.endswith("html"):
            s = tuple(parser.parse(directory_path))
            pp = ParseResult(s[0], s[-1], filename)
            pp.absolutePath = directory_path    #absolutna putanja do fajla
            parsiraniFilovi.append(pp)