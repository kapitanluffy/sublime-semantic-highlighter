from .block_analyzer import BlockAnalyzer


class PhpAnalyzer(BlockAnalyzer):
    syntax = 'php'

    def getClassScope(self):
        return 'meta.class entity.name.class'

    def getFunctionScope(self):
        return 'meta.function entity.name.function'

    def getGenericScope(self):
        return 'meta.block punctuation.section.block.begin | meta.embedded.block punctuation.section.block.begin'

    def getBlockScope(self, region):
        """
        Provides the scope of the block from the given region
        - Return None if symbol is a valid variable but no blocks found (global)
        - Return False if symbol is not a valid variable
        """

        # global constant inside a class method
        if super().matches(region, 'meta.class meta.function constant.other - constant.other.class'):
            return None

        # global constant inside a function
        if super().matches(region, 'meta.function constant.other - meta.class'):
            return None

        # global constant
        if super().matches(region, 'constant.other - meta.class - meta.function - constant.other.class'):
            return None

        # function variable
        if super().matches(region, 'meta.function variable.other - variable.other.member'):
            return 'meta.function.closure | meta.function entity.name.function'

        # function parameters
        if super().matches(region, 'meta.function.parameters variable.parameter'):
            return 'meta.function.closure | meta.function entity.name.function'

        # closures?
        if super().matches(region, 'meta.function.closure.use variable.parameter'):
            return 'meta.function.closure'

        # class property inside method
        if super().matches(region, 'meta.class variable.other.member'):
            return self.getClassScope()

        # class property declaration
        if super().matches(region, 'meta.class meta.block variable.other'):
            return self.getClassScope()

        # class constant declaration
        if super().matches(region, 'meta.class meta.block constant.other'):
            return self.getClassScope()

        # class variable?
        if super().matches(region, 'variable.other.class'):
            return self.getClassScope()

        # class constant?
        if super().matches(region, 'constant.other.class'):
            return self.getClassScope()

        if super().matches(region, 'variable.other | constant.other'):
            return None

        return False
