import sublime_plugin

from .highlight import SemanticHighlighterHighlightCommand
from ..symbol import Symbol


class SemanticHighlighterJumpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()[-1]
        highlighter = SemanticHighlighterHighlightCommand.getHighlighter(self.view)
        symbol = Symbol(self.view, selection)
        key = symbol.getKey()

        if key is False:
            return False

        scopedCollection = list(filter(lambda s : s.getKey() == symbol.getKey(), highlighter.collection))
        current = next(filter(lambda s : s.getRegion() == symbol.getRegion(), scopedCollection))
        index = scopedCollection.index(current) + 1

        if index >= len(scopedCollection):
            index = 0

        self.view.show_at_center(scopedCollection[index].getRegion())
        self.view.sel().clear()
        self.view.sel().add(scopedCollection[index].getRegion())

        return True
