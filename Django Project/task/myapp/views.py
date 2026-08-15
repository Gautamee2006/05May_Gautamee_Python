from django.shortcuts import render, redirect
from .models import userinfo

def index(request):
    if request.method == "POST":
        name = request.POST.get("name")

        user = userinfo.objects.create(name=name)

        return redirect("login", id=user.id)

    return render(request, "index.html")


def login(request, id):
    user = userinfo.objects.get(id=id)

    if request.method == "POST":
        user.age = request.POST.get("age")
        user.email = request.POST.get("email")
        user.mobile = request.POST.get("mobile")
        user.address = request.POST.get("address")
        user.save()

        

    return render(request, "login.html", {"user": user})

def showdata(request):
    data = userinfo.objects.all()
    return render(request, "showdata.html", {"data": data})


def updatedata(request, id):
    user = userinfo.objects.get(id=id)

    if request.method == "POST":
        user.name = request.POST.get("name")
        user.age = request.POST.get("age")
        user.email = request.POST.get("email")
        user.mobile = request.POST.get("mobile")
        user.address = request.POST.get("address")
        user.save()

        return redirect("showdata")

    return render(request, "update.html", {"user": user})


# Delete User
def deletedata(request, id):
    stid = userinfo.objects.get(id=id)
    userinfo.delete(stid)

    return redirect("showdata") 
    