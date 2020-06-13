from .block_analyzer import BlockAnalyzer


class JavascriptAnalyzer(BlockAnalyzer):
    syntax = 'javascript'

    def getClassScope(self):
        return 'meta.class entity.name.class'

    def getFunctionScope(self):
        return 'meta.function.declaration entity.name.function | meta.function.declaration storage.type.function'

    # @todo fix bisect uses closest scope causing invalid blocks
    def getBlockScope(self, region):
        """
        Provides the scope of the block from the given region
        - Return None if symbol is a valid variable but no blocks found (global)
        - Return False if symbol is not a valid variable
        """
        # variables inside function
        if super().matches(region, 'meta.function variable.other'):
            return self.getFunctionScope()

        # function parameters
        if super().matches(region, 'meta.function.declaration variable.parameter'):
            return self.getFunctionScope()

        # variable inside class
        if super().matches(region, 'meta.class variable.other'):
            return self.getClassScope()

        # class property declaration
        if super().matches(region, 'meta.class meta.property.object'):
            return self.getClassScope()

        # declared constants
        if super().matches(region, 'variable.other.constant'):
            return None

        # object literal keys
        if super().matches(region, 'meta.object-literal.key'):
            return None

        # object property
        if super().matches(region, 'meta.property.object'):
            return None

        # ignore language "constants"
        if super().matches(region, 'variable.function | variable.language | constant.language | constant.numeric'):
            return False

        if super().matches(region, 'variable | constant'):
            return None

        return False
