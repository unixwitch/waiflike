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


class SitePage(Page):
    body = models.TextField()
    search_name = "Text page"

    indexed_fields = ('body', )

    @property
    def rendered(self):
        return mark_safe(markdown.markdown(self.body,
            extensions=[ 'extra',
                         'codehilite',
                         waiflike.mdx_linker.LinkerExtension({
                             '__default__':  'waiflike.linkers.page',
                             'page:':        'waiflike.linkers.page', 
                             'image:':       'waiflike.linkers.image',
                         })
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
