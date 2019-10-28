import sublime
import sublime_plugin
from random import randrange
import inspect
import re

# global vars
settings = {}
syntax_scopes = {}
syntax = None
highlight_enabled = False
highlight_regions = {}
current_selection = None
highlight_tags = {}
selection_lock = False

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

def get_syntax(view):
    syntax = view.settings().get('syntax')
    match = re.match(r"\b(.+)\.sublime-syntax\b", syntax).group(1).split('/')
    syntax = match[len(match) - 1].lower()
    return syntax

def get_scopes(syntax):
    return syntax_scopes.get('base', []) + syntax_scopes.get(syntax, [])

class SemanticHighlightToggleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global highlight_enabled
        highlight_enabled = not highlight_enabled

        if (highlight_enabled):
            print("Highlighting enabled")
        if (not highlight_enabled):
            print("Highlighting diabled")

class SemanticHighlightSelectionCommand(sublime_plugin.TextCommand):
    scopes = []
    locked = False
    highlighted = None
    locked_highlighted = {}
    style = None
    key = None

    def run(self, edit, **kwargs):
        self.locked = kwargs.get('locked')

        syntax = get_syntax(self.view)
        scopes = get_scopes(syntax)
        self.scopes = ",".join(scopes)
        self.key = 'plugin.semantic_highlighter'

        styles = {
            'outline': sublime.DRAW_NO_FILL,
            'fill': sublime.DRAW_NO_OUTLINE,
            'underline': sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE | sublime.DRAW_SOLID_UNDERLINE
        }
        self.style = styles['underline']

        selection = self.view.sel()
        point = kwargs.get('point')
        if (point != None):
            selection.clear()
            selection.add(point)

        for region in selection:
            # ignore text selections
            if (region.size() > 0):
                continue

            highlighted = self.handle_region(region)

            if (highlighted == False):
                continue

            # if (self.locked == True):
            #     self.locked_highlighted[highlighted['word']] = highlighted
            #     continue

            # highlighted.highlight(lock)
            # highlighted.unhighlight()

            self.highlighted = highlighted

        return True

    def handle_region(self, region):
        color = randrange(0, 144)
        target = self.get_word(region)
        key = self.key

        if (target == False):
            return False

        if (self.highlighted != None):
            if (target == self.highlighted['word'] and self.locked != True):
                return False

        if (self.locked == True):
            key = "%s.%s" % (key, target)

        instances = self.get_target_instances(target)
        regions = [region] + instances

        self.highlight(key, regions, color)
        highlighted = { "word": target, "key": key, "color": color, "locked": self.locked, "active": True }

        return highlighted

    def get_target_instances(self, target):
        instances = self.view.find_all(target, sublime.LITERAL)
        regions = []

        for region in instances:
            instance = self.get_word(region)

            if (instance != target):
                continue

            regions.append(region)

        return regions

    def get_word(self, region):
        region = self.view.word(region)

        if (region.empty()):
            return False

        if (self.is_scope_match(region, self.scopes) == False):
            return False

        word = self.view.substr(region).strip()

        if (word == ""):
            return False

        return word

    def is_scope_match(self, point, scopes):
        # p = self.view.text_point(w.a, w.b)
        midpoint = (point.a + point.b) / 2
        return self.view.match_selector(midpoint, scopes)

    def unhighlight(self, word):
        self.view.erase_regions(word['key'])

    def highlight(self, key, regions, color):
        self.view.add_regions(key, regions, 'plugin.semantic_highlighter.color' + str(color) , '', self.style)

    def want_event(self):
        return True

class SemanticHighlightMarkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("keyboard")
        self.view.run_command('semantic_highlight_selection', { "locked": True })

class SemanticHighlightListener(sublime_plugin.ViewEventListener):
    def on_selection_modified_async(self):
        self.view.run_command('semantic_highlight_selection')

    def on_query_context(self, key, operator, operand, match_all):
        return ("semantic_highlighter" == key)

    # def on_hover(self, point, zone):
        # if (zone == sublime.HOVER_TEXT):
            # self.view.run_command('semantic_highlight_selection', {"point": point})
