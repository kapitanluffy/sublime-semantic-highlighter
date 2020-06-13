from .block_analyzer import BlockAnalyzer
from .block_analyzer_factory import BlockAnalyzerFactory
from .generic_analyzer import GenericAnalyzer
from .php_analyzer import PhpAnalyzer
from .python_analyzer import PythonAnalyzer
from .javascript_analyzer import JavascriptAnalyzer

BlockAnalyzerFactory.register(GenericAnalyzer())
BlockAnalyzerFactory.register(PhpAnalyzer())
BlockAnalyzerFactory.register(PythonAnalyzer())
BlockAnalyzerFactory.register(JavascriptAnalyzer())

__all__ = [
    'BlockAnalyzer',
    'BlockAnalyzerFactory',
    'GenericAnalyzer',
    'PhpAnalyzer',
    'PythonAnalyzer',
    'JavascriptAnalyzer'
]
