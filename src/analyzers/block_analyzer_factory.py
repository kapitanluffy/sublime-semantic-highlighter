import re


class BlockAnalyzerFactory():
    view = None
    analyzers = {}

    def __init__(self, view):
        self.view = view

    def getBlock(self, region):
        syntax = self.getSyntax()
        analyzer = self.create(syntax)
        return analyzer.getBlock(region)

    def getBlockScope(self, region):
        syntax = self.getSyntax()
        analyzer = self.create(syntax)
        return analyzer.getBlockScope(region)

    def getSyntax(self):
        syntaxRegex = '/([^/]+)\\.sublime-syntax$'
        syntaxFile = self.view.settings().get('syntax', None)
        match = re.search(syntaxRegex, syntaxFile)

        if (match is not None):
            syntax = match.groups(0)[0]
            syntax = syntax.replace(" ", "_")
            return syntax.lower()

        return None

    def register(analyzer):
        syntax = analyzer.syntax
        BlockAnalyzerFactory.analyzers[syntax] = analyzer

    def create(self, syntax):
        if syntax in BlockAnalyzerFactory.analyzers:
            BlockAnalyzerFactory.analyzers[syntax].setView(self.view)
            return BlockAnalyzerFactory.analyzers[syntax]

        BlockAnalyzerFactory.analyzers['__GENERIC__'].setView(self.view)
        return BlockAnalyzerFactory.analyzers['__GENERIC__']
