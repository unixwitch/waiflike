import re

from django.db import models
from django.utils.safestring import mark_safe
from django.conf import settings

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel    

import markdown
import waiflike.mdx.linker
import waiflike.mdx.tables

class SitePage(Page):
    site_name = settings.SITE_NAME
    body = models.TextField()
    search_name = "Text page"

    indexed_fields = ('body', )

    @property
    def rendered(self):
        return mark_safe(markdown.markdown(self.body,
            extensions=[ 'extra',
                         'codehilite',
                         waiflike.mdx.tables.TableExtension(),
                         waiflike.mdx.linker.LinkerExtension({
                             '__default__':  'waiflike.linkers.page',
                             'page:':        'waiflike.linkers.page', 
                             'image:':       'waiflike.linkers.image',
                             'doc:':         'waiflike.linkers.document',
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
