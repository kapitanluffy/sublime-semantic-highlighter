import sublime
from .state import *

class ScopeAnalyzer():
    view = None

    def analyze(self, view, region):
        matching_blocks = ['meta.function', 'meta.class']

        for scope in matching_blocks:
            if view.match_selector(region.a, scope) == True:
                return self.get_region_scope(view, region, scope)

    def get_region_scope(self, view, region, block):
        self.view = view

        if block == 'meta.function':
            region_scope = self.get_token_via_scope(region, "meta.function entity.name.function")

        if block == 'meta.class':
            region_scope = self.get_token_via_scope(region, "meta.class entity.name.class")

        # scope = self.view.scope_name(region_scope.a)
        # region_scope_name = self.view.substr(self.view.word(region_scope))
        # print(region_scope, "\"%s\"" % region_scope_name, scope)
        return region_scope

    def get_token_via_scope(self, region, scope):
        line = self.view.line(region)
        match = None
        bofmax = 100000

        while True:
            if match != None:
                break

            tokens = self.tokenize_line(line)
            for token in tokens:
                is_matched = self.view.match_selector(token.a, scope)

                if (is_matched == True):
                    match = token
                    break

            line = self.view.line(sublime.Region(line.a - 1, line.a - 1))
            if (line.a < 0):
                break

            bofmax = bofmax - 1
            if (bofmax <= 0):
                print("get_token_via_scope() buffer overflow? break!")
                break

        return match

    def tokenize_line(self, line):
        current_size = 0
        start_point = line.a
        tokens = []
        bofmax = 100000

        while (line.size() > 0):
            word = self.view.word(sublime.Region(start_point, start_point))
            current_size = current_size + word.size()

            if current_size > line.size():
                break

            tokens.append(word)
            start_point = word.b + 1

            bofmax = bofmax - 1
            if (bofmax <= 0):
                print("tokenize_line() buffer overflow? break!")
                break

        return tokens
