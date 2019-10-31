import sublime
import sublime_plugin

from .src.state import *
from .src.commands import *
from .src.listeners import *

def plugin_loaded():
    print("Semantic Highlighter loaded")
    global settings, syntax_scopes

    settings = sublime.load_settings('SemanticHighlighter.sublime-settings')

    settings.clear_on_change('scopes')
    settings.add_on_change('scopes', plugin_loaded)

    if (settings.has('scopes')):
        syntax_scopes = settings.get('scopes', {})

def plugin_unloaded():
    print("semantic highlighter unloaded")

class SemanticHighlighterDebugCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        analyzer = ScopeAnalyzer();
        selection = self.view.sel()
        analyzer.guess_block(self.view, selection[0])

class SemanticHighlighterMarkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("keyboard")
        self.view.run_command('semantic_highlighter_highlight', { "locked": True })

