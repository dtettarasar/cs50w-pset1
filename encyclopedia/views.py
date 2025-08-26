from django.shortcuts import render

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):
    return render(request, "encyclopedia/create_entry.html", {
        "entries": util.list_entries()
    })

def view_entry(request, entry_title):

    print("entry_title: ")
    print(entry_title)

    entry_data = util.get_entry(entry_title)
    print(entry_data)

    return render(request, "encyclopedia/view_entry.html", {
        "entries": util.list_entries()
    })