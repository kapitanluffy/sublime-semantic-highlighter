import sublime
import sublime_plugin
from ..symbol import Symbol
from ..highlighter import Highlighter


class SemanticHighlighterViewEventListener(sublime_plugin.ViewEventListener):
    selection = None
    views = {}

    @classmethod
    def getHighlighter(cls, view):
        viewId = view.id()
        if viewId not in cls.views:
            cls.views[viewId] = Highlighter(view)

        return cls.views[viewId]

    def on_selection_modified_async(self):
        self.highlight()

    def highlight(self):
        selection = self.initSelection()

        if (selection is None):
            return

        # only use the last selection
        region = selection[-1]
        highlighter = SemanticHighlighterViewEventListener.getHighlighter(self.view)

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
