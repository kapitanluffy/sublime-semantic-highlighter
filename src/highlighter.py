import sublime
from random import randrange

class Highlighter():
    colorVariations = 144
    style = sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE | sublime.DRAW_SOLID_UNDERLINE

    def __init__(self, view, symbol=None):
        self.collection = {}
        self.symbol = None
        self.view = view

        if symbol is not None:
            self.init(symbol)

    def init(self, symbol):
        self.symbol = symbol
        instances = symbol.getInstances()
        blocks = {}

        # group all symbol instances by blocks
        for s in instances:
            if s.view.id() != self.view.id():
                raise Exception("Invalid view id")

            key = s.getKey()

            if key is False:
                continue

            if key not in blocks:
                blocks[key] = []

            blocks[key].append(s)

        for key, block in blocks.items():
            # print("key:", self.view.id(), key)
            self.collection[key] = block

    def setStyle(key):
        styles = {
            'outline': sublime.DRAW_NO_FILL,
            'fill': sublime.DRAW_NO_OUTLINE,
            'underline': sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE | sublime.DRAW_SOLID_UNDERLINE
        }

        if key not in styles:
            key = 'underline'

        Highlighter.style = styles[key]

    def highlight(self, symbol):
        self.init(symbol)
        # style = sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE | sublime.DRAW_SOLID_UNDERLINE
        colors = {}

        for key, symbols in self.collection.items():
            if key not in colors:
                colors[key] = self.getColor()

            color = 'plugin.semantic_highlighter.color%s' % (colors[key])

            regions = list(map(lambda s: s.getRegion(), symbols))
            self.view.add_regions(key, regions,  color, "", Highlighter.style)

    def clear(self):
        for key, symbol in self.collection.items():
            # print("clear:", self.view.id(), key)
            self.view.erase_regions(key)

        self.collection.clear()
        self.symbol = None

    def isEmpty(self):
        return len(self.collection) <= 0

    def isHighlighted(self, target):
        if len(self.collection) <= 0:
            return False

        word = self.view.substr(self.view.word(target)).strip()

        if self.symbol is None:
            return False

        # print("?", word, self.symbol.getWord(), (word == self.symbol.getWord()))
        return word == self.symbol.getWord()

    def getColor(self):
        """
        Return a random number that is equal to the number of variations
        """
        return randrange(0, self.colorVariations)
