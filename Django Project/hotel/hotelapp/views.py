from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about-us.html")

def blog_details(request):
    return render(request,"blog-details.html")

def blog(request):
    return render(request,"blog.html")

def contact(request):
    return render(request,"contact.html")

def main(request):
    return render(request,"main.html")

def room_details(request):
    return render(request,"room-details.html")

def rooms(request):
    return render(request,"rooms.html")

def services(request):
    return render(request,"services.html")