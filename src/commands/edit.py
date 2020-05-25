import sublime_plugin

from .highlight import SemanticHighlighterHighlightCommand
from ..symbol import Symbol


class SemanticHighlighterEditCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()[-1]
        highlighter = SemanticHighlighterHighlightCommand.getHighlighter(self.view)
        symbol = Symbol(self.view, selection)
        key = symbol.getKey()

        if key is False:
            return False

        for index, symbol in enumerate(highlighter.collection[key]):
            self.view.sel().add_all([symbol.getRegion()])

        return True
