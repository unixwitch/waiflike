from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from waiflike.models import SitePage

def source(request, slug):
    p = get_object_or_404(SitePage, slug = slug)
    return HttpResponse(p.body, content_type='text/plain')
