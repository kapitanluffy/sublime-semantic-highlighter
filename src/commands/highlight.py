import sublime
import sublime_plugin
from ..symbol import Symbol
from ..highlighter import Highlighter


class SemanticHighlighterHighlightCommand(sublime_plugin.TextCommand):
    views = {}

    def __init__(self, *args, **kwargs):
        super(SemanticHighlighterHighlightCommand, self).__init__(*args, **kwargs)
        self.selection = None

    @classmethod
    def getHighlighter(cls, view):
        viewId = view.id()
        if viewId not in cls.views:
            cls.views[viewId] = Highlighter(view)

        return cls.views[viewId]

    def run(self, edit, **kwargs):
        selection = self.initSelection()

        if (selection is None):
            return

        # only use the last selection
        region = selection[-1]
        highlighter = SemanticHighlighterHighlightCommand.getHighlighter(self.view)

        if highlighter.isHighlighted(region) is True:
            return

        if highlighter.isEmpty() is False:
            highlighter.clear()

        symbol = Symbol(self.view, region)
        block = symbol.getBlockScope()

        if block is False:
            return

        sublime.set_timeout_async(highlighter.highlight(symbol))
        self.selection = None

    def initSelection(self):
        """
        Initializes the selection. Mitigates triggering the command twice (when mouse up)
        @see https://github.com/sublimehq/sublime_text/issues/1254
        """
        if len(self.view.sel()) > 1:
            return None

        # capture selection if empty and selection is not the same
        if (self.selection is None or self.selection is not self.view.sel()):
            self.selection = self.view.sel()
            return None

        return self.selection
