import re
from .block_analyzer import BlockAnalyzer


class PythonAnalyzer(BlockAnalyzer):
    syntax = 'python'
    currentTabCount = 0

    def getClassScope(self):
        return 'meta.class entity.name.class'

    def getFunctionScope(self):
        return 'meta.function entity.name.function'

    def getGenericScope(self):
        return 'punctuation.section.block | punctuation.section.class.begin | punctuation.section.function.begin'

    def getPreviousLine(self, line):
        bofmax = self.bofmax

        while True:
            previous = super().getPreviousLine(line)

            if (previous is None):
                return None

            tabCount = self.getTabCount(previous)
            bofmax = bofmax - 1
            line = previous

            if (tabCount < self.currentTabCount):
                return previous

            if (bofmax <= 0):
                raise Exception("getPreviousLine() overflow? break!")

    def getTabCount(self, line):
        s = self.view.substr(line)
        result = re.match("^(\s+)", s)

        if (result is None):
            return 0

        return len(result.group(1))

    def getBlockScope(self, region):
        """
        Provides the scope of the block from the given region
        - Return None if symbol is a variable but no blocks found (global)
        - Return False if symbol is not a variable
        """
        line = self.view.line(region)
        self.currentTabCount = self.getTabCount(line)

        if super().matches(region, 'meta.function.parameters variable.parameter'):
            return self.getFunctionScope()

        if super().matches(region, 'meta.qualified-name meta.generic-name - (function | variable.function)'):
            if (self.currentTabCount == 0):
                return None

            fn = self.analyze(region, 'punctuation.section.function.begin')
            cl = self.analyze(region, 'punctuation.section.class.begin')

            if (fn is None and cl is None):
                return self.getGenericScope()

            if (fn is None and cl is not None):
                return self.getClassScope()

            if (fn is not None and cl is None):
                return self.getFunctionScope()

            crLine = self.view.rowcol(region.a)[0]
            fnLine = self.view.rowcol(fn.a)[0]
            clLine = self.view.rowcol(cl.a)[0]

            # print("ln: %s, fn: %s, cl: %s" % (crLine, fnLine, clLine))

            if (crLine - fnLine) < (crLine - clLine):
                return self.getFunctionScope()

            if (crLine - clLine) < (crLine - fnLine):
                return self.getClassScope()

        return False
