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
    highlighted = {}
    locked_highlighted = {}
    style = None
    key = 'plugin.semantic_highlighter'
    state = None
    symbols = {}
    scope_analyzer = None
    current_selection = set()

    def get_scopes(self):
        syntax = get_syntax(self.view)
        scopes = get_scopes(syntax)
        return ",".join(scopes)

    def get_words(self, selection):
        words = set()

        for region in selection:
            # ignore text selections
            if (region.size() > 0):
                continue

            word = self.get_word(region)
            words.add(word)

        return words

    def run(self, edit, **kwargs):
        global state
        self.locked = kwargs.get('locked')
        self.scopes = self.get_scopes()
        self.style = state['style']

        if self.state == None:
            self.state = state

        # only use last selection region
        selection = self.view.sel()
        selection = [selection[-1]]

        # words = self.get_words(selection)
        # current_highlighted_words = set(self.state['current_highlight'].keys())

        # if current_highlighted_words == words:
        #     print(current_highlighted_words, words)
        #     return False

        point = kwargs.get('point')
        if (point != None):
            selection.clear()
            selection.add(point)

        self.scope_analyzer = ScopeAnalyzer()
        # words = set()

        for region in selection:
            # ignore text selections
            if (region.size() > 0):
                continue

            target_word = self.get_word(region)
            highlights = self.handle_region(target_word)

            if (highlights == False):
                continue

            # if (self.locked == True):
            #     self.locked_highlighted[highlights['word']] = highlights
            #     continue

            # self.current_selection.add(target_word)
            self.state['current_highlight'][target_word] = highlights

            for k,h in highlights.items():
                # self.view.sel().add_all(h['regions'])
                self.highlight(h['key'], h['regions'], h['color'])

        return True

    def handle_region(self, target):
        # skip if target is in the highlighted
        if (target in self.state['current_highlight'] and self.locked != True):
            return False

        # clear higlighted regions
        self.unhighlight(target)

        # skip if not a valid "word", clear highlight if exists
        if (target == False):
            return False

        # if (self.locked == True):
        #     key = "%s.%s" % (key, target)

        key = self.key
        regions = self.get_target_instances(target)
        highlights = {}
        symbol_regions = {}
        symbols = {}

        for r in regions:
            region_scope = self.scope_analyzer.analyze(self.view, r)
            region_scope_name = "_global_"
            region_scope_region = self.view.substr(self.view.line(r))

            if (region_scope != None):
                region_scope_region = self.view.substr(self.view.line(region_scope))
                region_scope_name = self.view.substr(self.view.word(region_scope))

            symbol_key = "%s.%s.%s" % (key, region_scope_name, target)

            if symbol_key in symbols:
                color = symbols[symbol_key]

            if symbol_key not in symbols:
                color = randrange(0, 144)
                symbols[symbol_key] = color

            if symbol_key in symbol_regions:
                symbol_regions[symbol_key].append(r)

            if symbol_key not in symbol_regions:
                symbol_regions[symbol_key] = []
                symbol_regions[symbol_key].append(r)

            # print(r, "%s -> %s [%s]" % (region_scope_name, target, region_scope_region))
            highlights[symbol_key] = {
                "word": target,
                "key": symbol_key,
                "color": color,
                "locked": self.locked,
                "active": True,
                "regions": symbol_regions[symbol_key],
                "scope": region_scope
            }

        return highlights

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

    def unhighlight(self, target):
        deletables = set()

        # highlight_keys = list(self.state['current_highlight'])
        # for k in highlight_keys:
        #     if target == k:
        #         continue

        #     highlights = self.state['current_highlight'].pop(k)

        #     for wk,highlight in highlights.items():
        #         self.view.erase_regions(highlight['key'])

        for word,highlights in self.state['current_highlight'].items():
            if target == word:
                continue
            deletables.add(word)

            for key in highlights:
                highlight = highlights[key]
                # self.current_selection.remove(highlight['word'])
                self.view.erase_regions(highlight['key'])

        for word in deletables:
            del self.state['current_highlight'][word]

    def highlight(self, key, regions, color):
        self.view.add_regions(key, regions, 'plugin.semantic_highlighter.color' + str(color) , '', self.style)

    def want_event(self):
        return True
