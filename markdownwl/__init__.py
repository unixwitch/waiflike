from markdown import markdown
import re

def sub_object(m, extras):
    opts = []
    if m.group(3) != None and len(m.group(3)):
        opts = m.group(3).split('|')[1:]

    if m.group(1) in extras:
        return extras[m.group(1)](m.group(2), opts)

    return ''

def markdownwl(s, extra):
    return markdown(re.sub(r'<:([a-z]+:)?([^>|\n]+)(\|[^>|\n]+){0,}>', lambda x: sub_object(x, extra), s))
