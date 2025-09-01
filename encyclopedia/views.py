from django.shortcuts import render, redirect

from django import forms

from . import util

from markdown2 import Markdown

markdowner = Markdown()

class NewEntryForm(forms.Form):
    title = forms.CharField(label='title', max_length=50)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):
    return render(request, "encyclopedia/create_entry.html", {
        'form': NewEntryForm()
    })

def view_entry(request, entry_title):

    print("entry_title: ")
    print(entry_title)

    entry_data = util.get_entry(entry_title)
    # print(entry_data)

    if entry_data == None:

            return render(request, "encyclopedia/no_entry_found.html", {
            "entries": util.list_entries(),
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
        search_result_list = []
        search_request = request.POST['query']
        
        # If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.
        if search_request in entry_list:
            
            return redirect("encyclopedia:view_entry", entry_title=search_request)
        
        # If the query does not match the name of an encyclopedia entry, the user should instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring.
        # For example, if the search query were ytho, then Python should appear in the search results.
        
        for entry in entry_list:
            
            if search_request in entry:
                
                search_result_list.append(entry)
        
        if len(search_result_list) != 0:
            
            return render(request, "encyclopedia/search_results.html", {
                "entries": search_result_list
            })
            
        else:
            
                return render(request, "encyclopedia/no_entry_found.html", {
                "entries": util.list_entries()
            })
            
    
    else: 
        
        # As this view isn't supposed to be directly accessed, without a post request, we redirect to home if the user try to access to search page, outside of the search form
        return redirect("encyclopedia:index")