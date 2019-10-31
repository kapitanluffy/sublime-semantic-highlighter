import sublime
import sublime_plugin

from random import randrange
import inspect
import re

from ..state import *
from ..helpers import *
from ..scope_analyzer import ScopeAnalyzer

class SemanticHighlighterHighlightCommand(sublime_plugin.TextCommand):
    scopes = []
    locked = False
    highlighted = None
    locked_highlighted = {}
    style = None
    key = None
    state = {}
    symbols = {}
    scope_analyzer = None

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

        self.scope_analyzer = ScopeAnalyzer()

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
            self.state['current_highlight'] = highlighted

        return True

    def handle_region(self, region):
        color = randrange(0, 144)
        target = self.get_word(region)
        key = self.key

        # skip if not a valid "word", clear highlight if exists
        if (target == False):
            if (self.highlighted != None):
                self.unhighlight(self.highlighted)
                self.highlighted = None
            return False

        # skip if target is equal to the highlighted
        if (self.highlighted != None):
            if (target == self.highlighted['word'] and self.locked != True):
                return False

        if (self.locked == True):
            key = "%s.%s" % (key, target)

        instances = self.get_target_instances(target)
        regions = [region] + instances

        # for r in regions:
        #     region_scope = self.scope_analyzer.analyze(self.view, region)
        #     region_scope_name = self.view.substr(self.view.word(region_scope))
        #     symbol_key = "%s.%s" % (region_scope_name, target)

        #     if symbol_key in self.symbols:
        #         color = self.symbols[symbols]

        #     if symbol_key in self.symbols == False:
        #         self.symbols[symbols] = color

        self.highlight(key, regions, color)
        highlighted = { "word": target, "key": key, "color": color, "locked": self.locked, "active": True, "regions": regions }

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
