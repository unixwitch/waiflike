import re

from django.db import models
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist

from wagtail import wagtaildocs

import markdown
from markdown.util import AtomicString
from markdown.util import etree

class Linker:
    def run(self, name, optstr):
        try:
            text = name
            if len(optstr):
                text = optstr[0]

            doc = wagtaildocs.models.Document.objects.get(title = name)
            url = doc.url
            a = etree.Element('a')
            a.set('href', url)
            a.text = text
            return a;
        except ObjectDoesNotExist:
            return '[document %s not found]' % (name,)
