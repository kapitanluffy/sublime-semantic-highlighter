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

    def getSyntax(self):
        syntaxRegex = '/([^/]+)\\.sublime-syntax$'
        syntaxFile = self.view.settings().get('syntax', None)
        match = re.search(syntaxRegex, syntaxFile)

        if (match is not None):
            syntax = match.groups(0)[0]
            return syntax.lower()

        return None

    def register(analyzer):
        syntax = analyzer.syntax
        BlockAnalyzerFactory.analyzers[syntax] = analyzer

    def create(self, syntax):
        if syntax in BlockAnalyzerFactory.analyzers:
            BlockAnalyzerFactory.analyzers[syntax].view = self.view
            return BlockAnalyzerFactory.analyzers[syntax]

        BlockAnalyzerFactory.analyzers['__GENERIC__'].view = self.view
        return BlockAnalyzerFactory.analyzers['__GENERIC__']
