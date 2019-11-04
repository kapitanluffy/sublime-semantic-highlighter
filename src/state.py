import sublime

# global vars
settings = {}
syntax = None
highlight_enabled = False
highlight_regions = {}
current_selection = None
highlight_tags = {}
selection_lock = False

styles = {
    'outline': sublime.DRAW_NO_FILL,
    'fill': sublime.DRAW_NO_OUTLINE,
    'underline': sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE | sublime.DRAW_SOLID_UNDERLINE
}

state = {
    "syntax_scopes": {},
    "current_highlight": {}
}
