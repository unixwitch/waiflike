from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel    
from markupfield.fields import MarkupField

class SitePage(Page):
    body = MarkupField(default_markup_type='markdown')
    search_name = "Text page"

    indexed_fields = ('body', )

SitePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
]
