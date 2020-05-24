from .block_analyzer import BlockAnalyzer


class GenericAnalyzer(BlockAnalyzer):
    syntax = '__GENERIC__'

    def getClassScope(self):
        return 'meta.class entity.name.class'

    def getFunctionScope(self):
        return 'meta.function entity.name.function'

    def getGenericScope(self):
        return 'meta.block'

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
            return self.getFunctionScope()

        # function parameters
        if super().matches(region, 'meta.function.parameters variable.parameter'):
            return self.getFunctionScope()

        # class property inside method
        if super().matches(region, 'meta.class variable.other.member'):
            return self.getClassScope()

        # class property declaration
        if super().matches(region, 'meta.class meta.block variable.other'):
            return self.getClassScope()

        # class constant declaration
        if super().matches(region, 'meta.class meta.block constant.other'):
            return self.getClassScope()

        if super().matches(region, 'variable.other | constant.other'):
            return self.getGenericScope()

        return False
