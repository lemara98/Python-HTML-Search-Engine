
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


def parseFiles(abs_path, parser, parsiraniFilovi):
    for filename in os.listdir(abs_path):
        print(len(os.listdir(abs_path)))
        if len(os.listdir(abs_path)) == 1:
            director = os.path.join(abs_path,filename)
            if os.path.isdir(director) and len(parsiraniFilovi) == 0 :
                abs_path = director
                parseFiles(abs_path,parser,parsiraniFilovi)
                break
        print(os.path.relpath(filename, abs_path))
        directory_path = os.path.join(abs_path, filename)
        if os.path.isdir(directory_path):  #ako je datoteka onda se rekurzivno poziva funkcija
            parseFiles(directory_path,parser,parsiraniFilovi)
        elif filename.endswith("html"):
            s = tuple(parser.parse(directory_path))
            pp = ParseResult(s[0], s[-1], directory_path)
            parsiraniFilovi.append(pp)