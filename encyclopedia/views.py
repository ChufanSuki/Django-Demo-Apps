from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import util
from markdown2 import Markdown
import os, random
from django import forms
from django.urls import reverse


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def detail(request, entry):
    return render(request, "encyclopedia/detail.html", {
        "content": Markdown().convert(util.get_entry(entry)),
        "title": entry
    })
    

def search(request):
    try:
        search_content = request.POST['q']
    except KeyError:
        return render(request, 'encyclopeida/index.html')
    else:
        return HttpResponseRedirect(reverse('encyclopedia:result', args=(search_content,)))

def result(request, query):
    cond, entries = util.search(query)
    if cond == True:
        return HttpResponseRedirect(reverse('encyclopedia:title', args=entries))
    elif entries:
        return render(request, "encyclopedia/result.html", {
            "entries": entries
        })
    else:
        return HttpResponseRedirect(reverse('encyclopedia:index'))

def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        wiki = request.POST['wiki']
        if util.search(title):
            return HttpResponse("<h1>Error! Title already existed!<\h1>")
        else:
            with open(f'./entries/{title}.md', "w", encoding="utf-8") as  f:
                f.write(wiki)
            return HttpResponseRedirect(reverse('encyclopedia:index'))
    else:
        return render(request, "encyclopedia/create.html")

def edit(request, entry=None):
    if request.method == 'POST':
        title = entry
        try:
            wiki = request.POST['wiki']
        except KeyError:
            return HttpResponseRedirect(reverse('encyclopedia:index'))
        else:
            with open(f'./entries/{title}.md', "w", encoding="utf-8") as  f:
                    f.write(wiki)
            return HttpResponseRedirect(reverse('encyclopedia:index'))
    else:
        return render(request, 'encyclopedia/edit.html', {
            "title": entry,
            "content": util.get_entry(entry)
        })

def random_page(request):
    return HttpResponseRedirect(reverse('encyclopedia:title', args=[random.choice(util.list_entries())]))

    