from django.shortcuts import render
from django.http import HttpResponse
from . import util
from markdown2 import Markdown
import os


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def detail(request, entry):
    return HttpResponse(Markdown().convert(util.get_entry(entry)))

