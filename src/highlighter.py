import sublime
from random import randrange


class Highlighter():
    colorVariations = 144
    style = sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE | sublime.DRAW_SOLID_UNDERLINE

    def __init__(self, view, symbol=None):
        self.collection = []
        self.symbol = None
        self.view = view
        self.regions = {}
        self.colors = {}

        if symbol is not None:
            self.init(symbol)

    def init(self, symbol):
        self.symbol = symbol
        self.collection = symbol.getInstances()

    @staticmethod
    def setStyle(key):
        styles = {
            'outline': sublime.DRAW_NO_FILL,
            'fill': sublime.DRAW_NO_OUTLINE,
            'underline': sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE | sublime.DRAW_SOLID_UNDERLINE
        }

        if key not in styles:
            key = 'underline'

        Highlighter.style = styles[key]

    def highlightSymbol(self, symbol):
        key = symbol.getKey()

        if key is False or key is None:
            return

        if key not in self.colors:
            self.colors[key] = self.getColor()

        if key not in self.regions:
            self.regions[key] = []

        self.regions[key].append(symbol.getRegion())
        color = 'plugin.semantic_highlighter.color%s' % (self.colors[key])
        self.view.add_regions(key, self.regions[key], color, "", Highlighter.style)

    def highlight(self, symbol):
        self.init(symbol)
        self.regions = {}

        for s in self.collection:
            sublime.set_timeout_async(self.highlightSymbol(s))

    def clear(self):
        for symbol in self.collection:
            key = symbol.getKey()

            if key is not False:
                self.view.erase_regions(key)

        for key in self.regions.keys():
            self.view.erase_regions(key)

        self.symbol = None

    def isEmpty(self):
        return len(self.collection) <= 0

    def isHighlighted(self, target):
        if len(self.collection) <= 0:
            return False

        word = self.view.substr(self.view.word(target)).strip()

        if self.symbol is None:
            return False

        if word != self.symbol.getWord():
            return False

        for s in self.collection:
            if s.getKey() is self.symbol.getKey():
                return self.symbol

        return False

    def getColor(self):
        """
        Return a random number that is equal to the number of variations
        """
        return randrange(0, self.colorVariations)
