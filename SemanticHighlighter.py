import sublime
import os
from shutil import copyfile
from .src.commands.highlight import SemanticHighlighterHighlightCommand
from .src.commands.edit import SemanticHighlighterEditCommand
from .src.commands.jump import SemanticHighlighterJumpCommand
from .src.listeners.view_event import SemanticHighlighterViewEventListener
from .src.highlighter import Highlighter


def update_style():
    settings = sublime.load_settings('SemanticHighlighter.sublime-settings')
    Highlighter.setStyle(settings.get('style', 'underline'))


def update_color_scheme():
    preferences = sublime.load_settings('Preferences.sublime-settings')
    plugindir = os.path.join(sublime.packages_path(), 'SemanticHighlighter')

    if not os.path.exists(plugindir):
        os.mkdir(plugindir)

    scheme = preferences.get('color_scheme').split(os.path.sep)

    if scheme[-1] == preferences.get('color_scheme'):
        scheme = preferences.get('color_scheme').split('/')

    scheme = os.path.join(plugindir, scheme[-1])

    if os.path.exists(scheme):
        return

    template = sublime.load_resource('Packages/SemanticHighlighter/Template.sublime-color-scheme.json')
    file = open(scheme, "w+")
    file.write(template)
    file.close()


def plugin_loaded():
    settings = sublime.load_settings('SemanticHighlighter.sublime-settings')
    settings.add_on_change('style', update_style)

    preferences = sublime.load_settings('Preferences.sublime-settings')
    preferences.add_on_change('color_scheme', update_color_scheme)

    update_color_scheme()
    update_style()
    print("Semantic Highlighter loaded")


def plugin_unloaded():
    settings = sublime.load_settings('SemanticHighlighter.sublime-settings')
    settings.clear_on_change('style')

    preferences = sublime.load_settings('Preferences.sublime-settings')
    preferences.clear_on_change('color_scheme')


__all__ = [
    'SemanticHighlighterHighlightCommand',
    'SemanticHighlighterEditCommand',
    'SemanticHighlighterJumpCommand',
    'SemanticHighlighterViewEventListener'
]
