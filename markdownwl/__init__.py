from django.core.exceptions import ObjectDoesNotExist
from wagtail import wagtailimages
from markdown import markdown
import re

def sub_image(m):
    fname = m.group(1)
    opts = {}
    optstr = 'left'

    if m.group(2) != None:
        optstr = m.group(2)

    for opt in optstr.split('|'):
        if opt in ('left', 'right', 'fullwidth'):
            opts['style'] = opt

    try:
        image = wagtailimages.models.get_image_model().objects.get(file = 'original_images/' + fname)
    except ObjectDoesNotExist:
        return '(Image %s not found)' % (fname,)

    formatter = wagtailimages.formats.get_image_format(opts['style'])
    return formatter.image_to_html(image, '')
    
def markdownwl(s):
    return markdown(re.sub(r'<:image:([^| ]+)(\|[^| ]+){0,}>', sub_image, s))
