import sublime
import sublime_plugin
from ..symbol import Symbol
from ..highlighter import Highlighter
from threading import Timer


def debounce(wait):
    """ Decorator that will postpone a functions
        execution until after wait seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)
            try:
                debounced.t.cancel()
            except(AttributeError):
                pass
            debounced.t = Timer(wait, call_it)
            debounced.t.start()
        return debounced
    return decorator


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
        selection = self.view.sel()
        region = selection[-1]

        self.highlight(region)

    @debounce(0.25)
    def highlight(self, region):
        highlighter = SemanticHighlighterViewEventListener.getHighlighter(self.view)
        symbol = highlighter.isHighlighted(region)

        # make sure there are no highlights if highlighter is empty
        if highlighter.isEmpty() is False:
            highlighter.clear()

        if symbol is False:
            symbol = Symbol(self.view, region)

        block = symbol.getBlockScope()
        if block is False:
            return

        sublime.set_timeout_async(highlighter.highlight(symbol))
        self.selection = None
