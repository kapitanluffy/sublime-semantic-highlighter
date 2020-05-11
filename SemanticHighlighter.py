import imp
import sys

import sublime
import sublime_plugin

from .src import *

def plugin_loaded():
    settings = sublime.load_settings('SemanticHighlighter.sublime-settings')

    settings.clear_on_change('scopes')
    settings.clear_on_change('style')

    settings.add_on_change('scopes', plugin_loaded)
    settings.add_on_change('style', plugin_loaded)

    state['style'] = styles[settings.get('style', 'underline')]
    state['syntax_scopes'] = settings.get('scopes', {})

    print("Semantic Highlighter loaded")

def plugin_unloaded():
    settings = sublime.load_settings('SemanticHighlighter.sublime-settings')
    settings.clear_on_change('scopes')
    settings.clear_on_change('style')

class SemanticHighlighterDebugCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        analyzer = ScopeAnalyzer();
        selection = self.view.sel()
        analyzer.analyze(self.view, selection[0])

class SemanticHighlighterMarkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('semantic_highlighter_highlight', { "locked": True })
