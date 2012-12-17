"""QSyntaxHighlighter implementation
Uses syntax module for doing the job
"""

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QBrush, QColor, QFont, QSyntaxHighlighter, QTextCharFormat, QTextBlockUserData


class _TextBlockUserData(QTextBlockUserData):
    def __init__(self, data):
        QTextBlockUserData.__init__(self)
        self.data = data


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, syntax, *args):
        QSyntaxHighlighter.__init__(self, *args)
        self._syntax = syntax
        self._quteparserToQtFormat = {}
    
    @staticmethod
    def formatConverterFunction(format):
        qtFormat = QTextCharFormat()
        qtFormat.setForeground(QBrush(QColor(format.color)))
        qtFormat.setBackground(QBrush(QColor(format.background)))
        qtFormat.setFontItalic(format.italic)
        qtFormat.setFontWeight(QFont.Bold if format.bold else QFont.Normal)
        qtFormat.setFontUnderline(format.underline)
        qtFormat.setFontStrikeOut(format.strikeOut)

        return qtFormat
    
    def _setFormat(self, start, length, format):
        if format is None:
            return
        self.setFormat(start, length, format)

    def highlightBlock(self, text):
        if True:
            lineData, highlightedSegments = self._syntax.highlightBlock(text, self._prevData())
            
            currentPos = 0
            for length, format in highlightedSegments:
                self._setFormat(currentPos, length, format)
                currentPos += length
        else:
            lineData = self._syntax.parseBlock(text, self._prevData())
        self.setCurrentBlockUserData(_TextBlockUserData(lineData))
            

    def _prevData(self):
        prevBlock = self.currentBlock().previous()
        if prevBlock.isValid():
            dataObject = prevBlock.userData()
            if dataObject is not None:
                return dataObject.data
        return None
