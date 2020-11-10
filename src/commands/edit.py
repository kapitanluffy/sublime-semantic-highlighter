import sublime_plugin

from ..listeners.view_event import SemanticHighlighterViewEventListener
from ..symbol import Symbol


class SemanticHighlighterEditCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()[-1]
        highlighter = SemanticHighlighterViewEventListener.getHighlighter(self.view)
        symbol = Symbol(self.view, selection)
        key = symbol.getKey()

        if key is False:
            return False

        regions = []

        for s in highlighter.collection:
            if s.getKey() != key:
                continue
            regions.append(s.getRegion())

        self.view.sel().add_all(regions)

        return True
