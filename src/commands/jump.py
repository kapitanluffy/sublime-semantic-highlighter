import sublime_plugin

from .highlight import SemanticHighlighterHighlightCommand
from ..symbol import Symbol


class SemanticHighlighterJumpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()[-1]
        highlighter = SemanticHighlighterHighlightCommand.getHighlighter(self.view)
        symbol = Symbol(self.view, selection)
        key = symbol.getKey()

        current = next(filter(lambda s : s.getRegion() == symbol.getRegion(), highlighter.collection[key]))
        index = highlighter.collection[key].index(current) + 1

        if index >= len(highlighter.collection[key]):
            index = 0

        self.view.show_at_center(highlighter.collection[key][index].getRegion())
        self.view.sel().clear()
        self.view.sel().add(highlighter.collection[key][index].getRegion())

        return True
