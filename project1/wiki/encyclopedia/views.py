from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
import os

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
        if request.method == "POST":
            filepath = f"entries/{name}.md"
            with open(filepath, 'w') as file:

                file.write(request.POST.get("edit_content", ""))

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

def new_page(request):
    entry_created = False
    if request.method == "POST":
        title = request.POST.get("new_title", "")
        content = request.POST.get("new_content", "")

        list_entries = util.list_entries()
        if title in list_entries:
            return render(request, "encyclopedia/new_page.html", {
                "entry_created": entry_created,
                "incorrect": True
            })
        else:
            entry_created = True
            filepath = f"entries/{title}.md"

            with open(filepath, 'w') as file:
                file.write("#" + title + "\n\n")
                file.write(content)

            return HttpResponseRedirect(reverse(f"encyclopedia:entry", kwargs={'name': title}))

    return render(request, "encyclopedia/new_page.html", {
        "entry_created": entry_created,
        "incorrect": False
    })

def edit(request):
    current_url = request.POST.get("current_url", "")
    edit_entry = os.path.basename(current_url)

    with open(f"entries/{edit_entry}.md", "r") as md_file:
        entry_content = md_file.read()

    return render(request, "encyclopedia/edit.html", {
        "entry_name": edit_entry,
        "entry_content": entry_content
    })

def random(request):
    rand_entry = util.get_random_entry()
    return HttpResponseRedirect(reverse(f"encyclopedia:entry", kwargs={"name": rand_entry}))