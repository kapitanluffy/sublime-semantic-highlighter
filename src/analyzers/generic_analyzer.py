from .block_analyzer import BlockAnalyzer


class GenericAnalyzer(BlockAnalyzer):
    syntax = '__GENERIC__'

    def getBlockScope(self, region):
        """
        Provides the scope of the block from the given region
        - Return None if symbol is a valid variable but no blocks found (global)
        - Return False if symbol is not a valid variable
        """
        if super().matches(region, 'variable | constant'):
            return None

        return False
