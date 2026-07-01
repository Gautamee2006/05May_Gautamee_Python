from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,"home.html",{'name':'Gautamee'})

def music(request):
    return render(request,"music.html")