from django.shortcuts import render
import random
count=0
# Create your views here.
def index(request):
    return render(request,'index.html')

def context(request):

    name="Gautamee"
    age="20"
    city="rajkot"
    num=random.randint(1111,9999)
    global count
    count += 1

    frutis=['banana','apple','mango']

    return render(request,'context.html',{'name':name,'num':num,'count':count,'fruits':frutis,'age':age,'city':city})

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")