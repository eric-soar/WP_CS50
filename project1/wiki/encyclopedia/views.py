from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

class NewSearchForm(forms.Form):
    search_entry = forms.CharField()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


def entry(request, name):
    list_entries = util.list_entries()
    if name not in list_entries:
        return render(request, "encyclopedia/wrong_entry.html", {
            "wrong_entry": name
        })
    else:
        return render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(name),
        "entry_name": name,
        "markdown": util.convert_markdown(f"entries/{name}.md")
    })


def search(request):
    if request.method == "POST":
        typed_entry = request.POST.get('typed_entry', '')
        entry_content = util.get_entry(typed_entry)

        if entry_content is not None:
            return HttpResponseRedirect(reverse(f"encyclopedia:entry", kwargs={'name': typed_entry}))
        else:
            list_entries = util.list_entries()
            matching_entry = "NOTHING FOUND"
            match = False
            for entry in list_entries:
                if typed_entry in entry:
                    matching_entry = entry
                    match = True
            return render(request, "encyclopedia/search_results.html", {
                "wrong_entry": typed_entry,
                "entries": list_entries,
                "matching_entry": matching_entry,
                "match": match
            })