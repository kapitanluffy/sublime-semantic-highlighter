import sublime_plugin

from ..listeners.view_event import SemanticHighlighterViewEventListener
from ..syntax_symbol import SyntaxSymbol


class SemanticHighlighterJumpCommand(sublime_plugin.TextCommand):
    scopedCollection = None

    def run(self, edit):
        selection = self.view.sel()[-1]
        highlighter = SemanticHighlighterViewEventListener.getHighlighter(self.view)
        symbol = SyntaxSymbol(self.view, selection)
        key = symbol.getKey()

        if key is False:
            return False

        if SemanticHighlighterJumpCommand.scopedCollection is None:
            SemanticHighlighterJumpCommand.scopedCollection = list(filter(lambda s : s.getKey() == symbol.getKey(), highlighter.collection))

        scopedCollection = SemanticHighlighterJumpCommand.scopedCollection
        current = next(filter(lambda s : s.getRegion() == symbol.getRegion(), scopedCollection))
        index = scopedCollection.index(current) + 1

        if index >= len(scopedCollection):
            index = 0

        self.view.show_at_center(scopedCollection[index].getRegion())
        self.view.sel().clear()
        self.view.sel().add(scopedCollection[index].getRegion())

        return True
