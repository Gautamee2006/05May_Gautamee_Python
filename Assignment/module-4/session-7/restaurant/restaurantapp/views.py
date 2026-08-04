from django.shortcuts import render
from .forms import RestaurantForm

def add_restaurant(request):

    if request.method == "POST":
        form = RestaurantForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, "success.html")

    else:
        form = RestaurantForm()

    return render(request, "add_restaurant.html", {"form": form})