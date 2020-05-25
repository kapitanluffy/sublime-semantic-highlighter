import sublime
import os
from .src.commands.highlight import SemanticHighlighterHighlightCommand
from .src.commands.edit import SemanticHighlighterEditCommand
from .src.commands.jump import SemanticHighlighterJumpCommand
from .src.listeners.view_event import SemanticHighlighterViewEventListener
from .src.highlighter import Highlighter


def update_plugin_settings():
    """
    Watch for plugin settings changes
    """
    settings = sublime.load_settings('SemanticHighlighter.sublime-settings')
    Highlighter.setStyle(settings.get('style', 'underline'))


def update_preferences():
    """
    Watch for color_scheme changes
    """
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
    settings.add_on_change('plugin.semantic-highlighter', update_plugin_settings)

    preferences = sublime.load_settings('Preferences.sublime-settings')
    preferences.add_on_change('plugin.semantic-highlighter', update_preferences)

    update_preferences()
    update_plugin_settings()
    print("Semantic Highlighter loaded")


def plugin_unloaded():
    settings = sublime.load_settings('SemanticHighlighter.sublime-settings')
    settings.clear_on_change('plugin.semantic-highlighter')

    preferences = sublime.load_settings('Preferences.sublime-settings')
    preferences.clear_on_change('plugin.semantic-highlighter')


__all__ = [
    'SemanticHighlighterHighlightCommand',
    'SemanticHighlighterEditCommand',
    'SemanticHighlighterJumpCommand',
    'SemanticHighlighterViewEventListener'
]
