import sublime
import sublime_plugin

from ..state import *
from ..helpers import *
from ..scope_analyzer import *

class SemanticHighlighterEditCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        selection = selection[-1]

        region = self.view.word(selection)
        word = self.view.substr(region)

        if word not in state['current_highlight']:
            return False

        scope_analyzer = ScopeAnalyzer()
        scope = scope_analyzer.analyze(self.view, region)
        scope = self.region_to_string(scope)

        for key,highlight in state['current_highlight'][word].items():
            highlight_scope = self.region_to_string(highlight['scope'])

            if (highlight_scope != scope):
                continue

            self.view.sel().add_all(highlight['regions'])

    def region_to_string(self, region):
        if region == None:
            return False

        region = self.view.word(region)
        return self.view.substr(region)
