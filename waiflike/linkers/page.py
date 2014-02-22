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

from waiflike.models import SitePage

class Linker:
    def run(self, name, optstr):
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
            return '[page %s not found]' % (name,)
