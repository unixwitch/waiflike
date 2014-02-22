import re

from django.db import models
from django.utils.safestring import mark_safe

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel    
from markupfield.fields import MarkupField
import markdownwl
from django.core.exceptions import ObjectDoesNotExist
from wagtail import wagtailimages

def sub_image(fname, optstr):
    opts = {}

    for opt in optstr:
        if opt in ('left', 'right', 'fullwidth'):
            print opt
            opts['style'] = opt

    try:
        image = wagtailimages.models.get_image_model().objects.get(title = fname)
    except ObjectDoesNotExist:
        return '[image %s not found]' % (fname,)

    formatter = wagtailimages.formats.get_image_format(opts['style'])
    return formatter.image_to_html(image, '')

def sub_page(name, optstr):
    try:
        text = name
        if len(optstr):
            text = optstr[0]

        page = SitePage.objects.get(title = name)
        url = page.url
        return '<a href="%s">%s</a>' % (url, text)
    except ObjectDoesNotExist:
        return '[page %s not found]' % (name,)

def wl_markdown(s):
    return markdownwl.markdownwl(s, MARKDOWN_EXTRAS)

MARKDOWN_EXTRAS = {
    '': sub_page,
    'page:': sub_page,
    'image:': sub_image
}

class SitePage(Page):
    body = MarkupField(markup_choices = (('markdown', wl_markdown),))
    search_name = "Text page"

    indexed_fields = ('body', )

SitePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
]
