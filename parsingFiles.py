
import os

class ParseResult:
    def __init__(self, links, words, name):
        self.links = links
        self.words = words
        self.name = name


def parseFiles(abs_path, parser, parsiraniFilovi):
    for filename in os.listdir(abs_path):
        print(filename)
        directory_path = os.path.join(abs_path, filename)

        if os.path.isdir(directory_path):  #ako je datoteka onda se rekurzivno poziva funkcija
            parseFiles(directory_path,parser,parsiraniFilovi)
        if filename.endswith("html"):
            s = tuple(parser.parse(directory_path))
            pp = ParseResult(s[0], s[-1], filename)
            pp.absolutePath = directory_path    #absolutna putanja do fajla
            parsiraniFilovi.append(pp)