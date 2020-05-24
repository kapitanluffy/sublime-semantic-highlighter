import sublime
from .analyzers import BlockAnalyzerFactory


class Symbol():
    view = None
    target = None
    blockAnalyzer = None
    instances = []
    block = None

    def __init__(self, view, target):
        self.view = view
        self.target = self.view.word(target)   # normalize selection region
        self.blockAnalyzer = BlockAnalyzerFactory(self.view)
        return

    def getKey(self):
        block = self.getBlock()

        if block is False:
            raise Exception("Invalid symbol")

        target = self.getWord()
        view = self.view.id()

        key = "%s.%s.%s.%s.%s" % ("plugin.semantic_highlighter", block.a, block.b, target, view)
        return key

    def getWord(self):
        # w = self.view.word(self.target)
        return self.view.substr(self.target).strip()

    def getRegion(self):
        return self.target

    def getBlock(self):
        if self.block is None:
            self.block = self.blockAnalyzer.getBlock(self.target)

        return self.block

    def getInstances(self):
        # word = self.view.word(self.target)
        string = self.view.substr(self.target).strip()
        instances = self.view.find_all(string, sublime.LITERAL)
        # targets = [Symbol(self.view, word)]
        targets = [self]

        for instance in instances:
            # skip the target instance
            if instance.a == self.target.a and instance.b == self.target.b:
                continue

            r = self.view.word(instance)
            s = self.view.substr(r).strip()
            if (s != string):
                continue

            symbol = Symbol(self.view, instance)
            if symbol.getBlock() is not False:
                targets.append(symbol)

        return targets
