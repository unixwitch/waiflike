import markdown
from markdown.util import AtomicString
from markdown.util import etree

LINKER_RE = r'<:([a-z]+:)?([^>|\n]+)((\|[^>|\n]+){0,})>'

class LinkerPattern(markdown.inlinepatterns.Pattern):
    def __init__(self, re, md, linktypes):
        markdown.inlinepatterns.Pattern.__init__(self, re, md)
        self.linktypes = linktypes

    def handleMatch(self, m):
        linktypes = self.linktypes
        opts = []
        if m.group(3) != None and len(m.group(4)):
            opts = m.group(4).split('|')[1:]

        if m.group(2) == None and '__default__' in linktypes:
            return linktypes['__default__'](m.group(3), opts)
        elif m.group(2) in linktypes:
            return linktypes[m.group(2)](m.group(3), opts)

        return AtomicString('[invalid link]')

class LinkerExtension(markdown.Extension):
    def __init__(self, linktypes):
        markdown.Extension.__init__(self)
        self.linktypes = linktypes

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['linker'] = LinkerPattern(LINKER_RE, md, self.linktypes)

def makeExtension(configs=None):
    return LinkerExtension(configs=configs)
