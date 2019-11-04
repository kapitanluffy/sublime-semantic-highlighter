import sublime
import sublime_plugin

import re

from .state import *

def get_syntax(view):
    syntax = view.settings().get('syntax')
    match = re.match(r"\b(.+)\.(sublime-syntax|tmLanguage)\b", syntax).group(1).split('/')
    syntax = match[len(match) - 1].lower()
    return syntax

def get_scopes(syntax):
    return state['syntax_scopes'].get('base', []) + state['syntax_scopes'].get(syntax, [])

def get_region_string(region, line = False):
    v = sublime.active_window().active_view()
    r = v.line(region) if line else v.word(region)
    return v.substr(r)
