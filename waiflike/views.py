from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from waiflike.models import SitePage

def source(request, slug):
    p = get_object_or_404(SitePage, slug = slug)
    return render(request, 'waiflike/source.html',
        dictionary = { 'page': p })

class EditForm(forms.Form):
    body = forms.CharField(widget = forms.Textarea)

def edit(request, slug):
    if not request.user.is_authenticated():
        raise PermissionDenied

    p = get_object_or_404(SitePage, slug = slug)

    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            p.body = form.cleaned_data['body']
            p.save()
            return HttpResponseRedirect(p.url)
    else:
        form = EditForm(initial = { 'body': p.body })

    return render(request, 'waiflike/edit.html',
        dictionary =  {
            'page': p,
            'form': form
        })
