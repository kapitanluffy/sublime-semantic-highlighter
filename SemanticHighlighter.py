import sublime
import os
import re
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
    SemanticHighlighterViewEventListener.delay = settings.get('delay', 0.25)


def remove_generated_color_schemes(plugindir):
    colorSchemes = sublime.find_resources('*.sublime-color-scheme')

    for colorScheme in colorSchemes:
        match = re.match('Packages/Semantic Highlighter/(.+\.sublime-color-scheme)', colorScheme)

        if match is not None:
            f = os.path.join(plugindir, match.group(1))

            if os.path.exists(f):
                print("Remove color scheme", f)
                os.remove(f)


def update_preferences():
    """
    Watch for color_scheme changes
    """
    preferences = sublime.load_settings('Preferences.sublime-settings')
    plugindir = os.path.join(sublime.packages_path(), 'Semantic Highlighter')

    if not os.path.exists(plugindir):
        os.mkdir(plugindir)

    scheme = preferences.get('color_scheme').split(os.path.sep)

    if scheme[-1] == preferences.get('color_scheme'):
        scheme = preferences.get('color_scheme').split('/')

    filename, fileext = os.path.splitext(scheme[-1]);
    filename = os.path.join(plugindir, filename)
    filename = "%s.sublime-color-scheme" % filename

    if os.path.exists(filename):
        return

    remove_generated_color_schemes(plugindir)
    template = sublime.load_resource('Packages/Semantic Highlighter/Template.hidden-color-scheme')
    file = open(filename, "w+")
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
    'SemanticHighlighterEditCommand',
    'SemanticHighlighterJumpCommand',
    'SemanticHighlighterViewEventListener'
]
