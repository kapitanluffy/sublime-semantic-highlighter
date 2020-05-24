import sublime


class BlockAnalyzer():
    view = None
    bofmax = 1000

    def __init__(self, view=None):
        self.view = view

    def getBlock(self, region):
        """
        Provides the region of the block from the given target region
        - Return None if no blocks found (global)
        - Return False if region is not a valid variable
        """

        scope = self.getBlockScope(region)

        if scope is None:
            return sublime.Region(0, 0)

        if (scope is False):
            return False

        block = self.analyze(region, scope)

        if block is None:
            return sublime.Region(0, 0)

        # should I really do this though?
        if block is not None:
            self.view.unfold(block)

        return block

    def analyze(self, region, scope):
        """
        Scan previous characters starting from the target region
        to check if it matches the provided scope
        """
        line = self.getLine(region)
        bofmax = self.bofmax

        while True:
            # print("line: %s" % (self.view.substr(line)))
            tokens = self.tokenize(line)
            # print("tokens: %s" % (tokens))
            for token in tokens:
                # print("token: %s" % (self.view.substr(token)))
                if (self.view.match_selector(token.a, scope)):
                    return token

            line = self.getPreviousLine(line)

            if (line is None):
                return None

            bofmax = bofmax - 1
            if (bofmax <= 0):
                raise Exception("getBlock() overflow? break!")

        return False

    def getPreviousLine(self, line):
        """
        Get the previous line
        """
        previous = sublime.Region(line.a - 1, line.a - 1)
        line = self.getLine(previous)

        if (line.a <= 0):
            return None

        return line

    def tokenize(self, line):
        """
        Split the line into non-empty characters
        """
        tokens = []
        totalSize = 0
        start = sublime.Region(line.a, line.a)

        while (totalSize <= line.size()):
            # return all tokens if total size is longer than the line
            totalSize = totalSize + 1

            if self.view.substr(start).strip() != "":
                tokens.append(start)

            # start to the next character after last word
            start = sublime.Region(start.b, start.b + 1)

        return tokens

    def getLine(self, region):
        """
        Get the line region of the target region
        """
        return self.view.line(region)

    def matches(self, region, scope):
        """
        Check if starting point of target region matches the scope
        """
        return self.view.match_selector(region.a, scope)
