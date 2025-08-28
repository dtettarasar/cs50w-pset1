from django.shortcuts import render

from . import util

from markdown2 import Markdown

markdowner = Markdown()

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

    if entry_data == None:

            return render(request, "encyclopedia/no_entry_found.html", {
            "entries": util.list_entries()
        })
    
    else:

        return render(request, "encyclopedia/view_entry.html", {
            "entry_title": entry_title,
            "entry_data": markdowner.convert(entry_data),
        })

def search_entry(request):
    
    if request.method == "POST":
        
        # print("search request:")
        # print(request.POST)
        
        search_request = request.POST['query']
        print("search_request: ")
        print(search_request)
        
        entry_data = util.get_entry(search_request)
        print(entry_data)
        
        # return render(request, "encyclopedia/search_results.html")
        
        if entry_data == None:
            
            return render(request, "encyclopedia/no_entry_found.html", {
            "entries": util.list_entries()
        })
            
        else:
            
            return render(request, "encyclopedia/search_results.html")
            
    
    else: 
        
        return render(request, "encyclopedia/no_entry_found.html", {
            "entries": util.list_entries()
        })