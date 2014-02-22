import re

from django.db import models
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel    
from wagtail import wagtailimages

import markdown
from markdown.util import AtomicString
from markdown.util import etree
import waiflike.mdx_linker

def sub_image(fname, optstr):
    opts = {}

    opts['spec'] = 'width-500'
    opts['classname'] = 'left'

    for opt in optstr:
        bits = opt.split('=', 1)
        opt = bits[0]
        value = ''

        if len(bits) > 1:
            value = bits[1]

        if opt == 'left':
            opts['classname'] = 'left'
        elif opt == 'right':
            opts['classname'] = 'right'
        elif opt == 'full':
            opts['classname'] = 'full-width'
        elif opt == 'width':
            try:
                opts['spec'] = "width-%d" % int(value)
            except ValueError:
                pass
    try:
        image = wagtailimages.models.get_image_model().objects.get(title = fname)
    except ObjectDoesNotExist:
        return '[image %s not found]' % (fname,)

    url = image.file.url
    rendition = image.get_rendition(opts['spec'])

    a = etree.Element('a')
    a.set('data-toggle', 'lightbox')
    a.set('data-type', 'image')
    a.set('href', image.file.url)
    img = etree.SubElement(a, 'img')
    img.set('src', rendition.url)
    img.set('class', opts['classname'])
    img.set('width', str(rendition.width))
    img.set('height', str(rendition.height))
    return a

def sub_page(name, optstr):
    try:
        text = name
        if len(optstr):
            text = optstr[0]

        page = SitePage.objects.get(title = name)
        url = page.url
        a = etree.Element('a')
        a.set('href', url)
        a.text = text
        return a;
    except ObjectDoesNotExist:
        return AtomicString('[page %s not found]' % (name,))

def wl_markdown(s):
    return markdownwl.markdownwl(s, MARKDOWN_EXTRAS)

MARKDOWN_EXTRAS = {
    '__default__': sub_page,
    'page:': sub_page,
    'image:': sub_image
}

class SitePage(Page):
    body = models.TextField()
    search_name = "Text page"

    indexed_fields = ('body', )

    @property
    def rendered(self):
        return mark_safe(markdown.markdown(self.body,
            extensions=[ 'extra',
                         'codehilite',
                         waiflike.mdx_linker.LinkerExtension(MARKDOWN_EXTRAS),
                       ], 
            extension_configs = { 
                'codehilite': [ 
                    ('guess_lang', False),
                ]
            }, output_format='html5'))

SitePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
]
