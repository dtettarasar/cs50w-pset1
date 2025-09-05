from django.shortcuts import render, redirect

from django import forms

from django.core.exceptions import ValidationError

from . import util

from markdown2 import Markdown

markdowner = Markdown()

class NewEntryForm(forms.Form):
    
    title = forms.CharField(label='title', max_length=50)
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":8, "cols":10}))
    
    def clean_title(self):
        
        data = self.cleaned_data["title"]
        
        # When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
        entry_list = util.list_entries()
        
        if data in entry_list:
            
            raise ValidationError('Error: This title is already used for another entry')
        
        return data

class EditEntryForm(forms.Form):
    
    title = forms.CharField(label='title', max_length=50, disabled=True)
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":8, "cols":10}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):
    
    if request.method == "POST":
        
        form = NewEntryForm(request.POST)
        
        if form.is_valid():
            
            form_data = {
                
                'title': form.cleaned_data['title'],
                'body' : form.cleaned_data['body']
                
            }
            
            # print('form_data: ')
            # print(form_data)
            
            # The encyclopedia entry should be saved to disk, and the user should be taken to the new entry’s page.
            util.save_entry(form_data["title"], form_data["body"])
            return redirect("encyclopedia:view_entry", entry_title=form_data["title"])
        
        else:
            
            return render(request, "encyclopedia/create_entry.html", {
                'form': form
            })
        
    else:
        
        form = NewEntryForm()
    
    
    return render(request, "encyclopedia/create_entry.html", {
        'form': form
    })

def edit(request, entry_title):
    
    print("accessing edit entry page")
    print("entry_title: ")
    print(entry_title)
    
    entry_data = util.get_entry(entry_title)
    
    
    if request.method == "POST":
        
        print("accessing edit entry page (POST Method)")
        
        form = EditEntryForm(request.POST)
        
        if form.is_valid():
            
            print("ok: form value valid")
            
            form_data = {
                
                'title': form.cleaned_data['title'],
                'body' : form.cleaned_data['body']
                
            }
            
            print('form_data: ')
            print(form_data)
            
        else:
            
            print("error: form value not valid")
            print(form.errors.as_data())
            
            form = EditEntryForm(initial={"title": entry_title, "body": entry_data})
            
            return render(request, "encyclopedia/edit_entry.html", {
                'form': form,
                'entry_title': entry_title
            })
            
    else: 
        
        form = EditEntryForm(initial={"title": entry_title, "body": entry_data})
    
    
    return render(request, "encyclopedia/edit_entry.html", {
        'form': form,
        'entry_title': entry_title
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