import sublime_plugin


class SemanticHighlighterViewEventListener(sublime_plugin.ViewEventListener):
    def on_selection_modified_async(self):
        self.view.run_command('semantic_highlighter_highlight')
