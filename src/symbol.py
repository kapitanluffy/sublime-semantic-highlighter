import sublime
from .analyzers import BlockAnalyzerFactory


class Symbol():
    view = None
    target = None
    targetString = None
    blockAnalyzer = None
    instances = []
    block = None
    blockScope = None

    def __init__(self, view, target):
        self.view = view
        self.target = self.view.word(target.a)   # normalize selection region
        self.targetString = self.view.substr(self.target).strip()
        self.blockAnalyzer = BlockAnalyzerFactory(self.view)

    def getKey(self):
        scope = self.getBlockScope()

        if scope is False:
            return False

        block = self.getBlock()

        if block is False:
            return False

        view = self.view.id()

        key = "%s.%s.%s.%s.%s" % ("plugin.semantic_highlighter", block.a, block.b, self.targetString, view)
        return key

    def getWord(self):
        return self.view.substr(self.target).strip()

    def getRegion(self):
        return self.target

    def getBlock(self):
        if self.block is None:
            self.block = self.blockAnalyzer.getBlock(self.target)

        return self.block

    def getBlockScope(self):
        if self.blockScope is None:
            self.blockScope = self.blockAnalyzer.getBlockScope(self.target)

        return self.blockScope

    def getInstances(self):
        string = self.view.substr(self.target).strip()
        instances = self.view.find_all(string, sublime.LITERAL)
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

            if symbol.getBlockScope() is not False:
                targets.append(symbol)

        return targets
