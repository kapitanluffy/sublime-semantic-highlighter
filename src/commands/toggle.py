import sublime
import sublime_plugin

from ..state import *
from ..helpers import *

class SemanticHighlightToggleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global highlight_enabled
        highlight_enabled = not highlight_enabled

        if (highlight_enabled):
            print("Highlighting enabled")
        if (not highlight_enabled):
            print("Highlighting diabled")
