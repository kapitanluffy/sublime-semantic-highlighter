import sublime_plugin


class SemanticHighlighterViewEventListener(sublime_plugin.ViewEventListener):
    def on_selection_modified_async(self):
        self.view.run_command('semantic_highlighter_highlight')

    def on_query_context(self, context, operator, operand, match_all):
        """
        run highlighter if context matches
        """
        if ("semantic_highlighter" == context):
            return True

        return None
