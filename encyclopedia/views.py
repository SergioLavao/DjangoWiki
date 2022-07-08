import random
from django.shortcuts import render,redirect
from django.http import HttpResponse   
from markdown2 import Markdown  

from . import util

def index(request):
    entries = util.list_entries()   
    if request.method == "POST":    
        search_by = request.POST.get('searchby')   
        if util.get_entry(search_by):
            return redirect(f'wiki/{search_by}')   
        return render(request, "encyclopedia/results.html", {
            "search_by": search_by,
            "entries": filter(lambda x: f'{search_by}' in x, entries)    
        })

    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def wiki(request, title):
    page = util.get_entry(title) 
    if not page:
        return render(request,"encyclopedia/error.html",{
            "error": "Error 404!",
            "info" : "Page was not found"
        })       
    if request.GET.get('edit'):
        return render(request,"encyclopedia/edit.html",{ "title": title, "content": page})  
    if request.method == "POST":  
        page = request.POST.get('content')  
        util.save_entry(title, page) 
    page = Markdown().convert(page) 
    return render(request,"encyclopedia/wiki.html",{"wiki_name": title, "wiki": page})  

def add(request):
    if request.method == "POST":  
        title = request.POST.get('title')   
        if util.get_entry(title): #Verify if article already exists.
            return render(request,"encyclopedia/error.html",{
            "error": "Error 409!",
            "info" : "This article already exists"
            })    
        util.save_entry(title, request.POST.get('content')) 
        return redirect(f'wiki/{title}') #Redirect to new wiki page.
    return render(request,"encyclopedia/new_edit.html")

def random_wiki(request):
    return redirect(f'wiki/{random.choice(util.list_entries())}')  