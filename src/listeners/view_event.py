import sublime
import sublime_plugin

from ..state import *
from ..helpers import *

class SemanticHighlighterViewEventListener(sublime_plugin.ViewEventListener):
    def on_selection_modified_async(self):
        self.view.run_command('semantic_highlighter_highlight')

    def on_query_context(self, key, operator, operand, match_all):
        return ("semantic_highlighter" == key)

    # def on_hover(self, point, zone):
        # if (zone == sublime.HOVER_TEXT):
            # self.view.run_command('semantic_highlighter_highlight', {"point": point})
