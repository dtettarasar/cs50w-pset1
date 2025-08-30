from django.shortcuts import render, redirect

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
    # print(entry_data)

    if entry_data == None:

            return render(request, "encyclopedia/no_entry_found.html", {
            "entries": util.list_entries()
        })
    
    else:

        return render(request, "encyclopedia/view_entry.html", {
            "entry_title": entry_title,
            "entry_data": markdowner.convert(entry_data),
        })

# Allow the user to type a query into the search box in the sidebar to search for an encyclopedia entry.
def search_entry(request):
    
    if request.method == "POST":
        
        entry_list = util.list_entries()
        
        print("entry_list")
        print(entry_list)
        
        search_result_list = []
        
        search_request = request.POST['query']
        print("search_request: ")
        print(search_request)
        
        entry_data = util.get_entry(search_request)
        
        # If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.
        if search_request in entry_list:
            
            print(f"Exact match: '{search_request}' is in entry_list")
            
            return redirect("encyclopedia:view_entry", entry_title=search_request)
        
        # If the query does not match the name of an encyclopedia entry, the user should instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring.
        # For example, if the search query were ytho, then Python should appear in the search results.
        
        for entry in entry_list:
            
            if search_request in entry:
                
                search_result_list.append(entry)
        
        # print('search_result_list')
        # print(search_result_list)
        
        if len(search_result_list) != 0:
            
            return render(request, "encyclopedia/search_results.html", {
                "entries": search_result_list
            })
            
    
    else: 
        
        return render(request, "encyclopedia/no_entry_found.html", {
            "entries": util.list_entries()
        })