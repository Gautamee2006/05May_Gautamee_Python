import csv
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Profile
from .forms import ProfileForm

def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'profiles/profile_list.html', {'profiles': profiles})

def profile_create(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile_list')
    else:
        form = ProfileForm()
    return render(request, 'profiles/profile_form.html', {'form': form})

def profile_edit(request, id):
    profile = get_object_or_404(Profile, id=id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_list')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/profile_form.html', {'form': form, 'profile': profile})

def profile_export(request):
    profiles = Profile.objects.all()
    temp_filename = 'profiles_export_temp.csv'
    
    # Using Context Manager with open(...) as file: as required by the assignment
    with open(temp_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Username', 'Email', 'Age', 'Bio', 'Is Public'])
        for p in profiles:
            writer.writerow([p.id, p.username, p.email, p.age, p.bio, p.is_public])

    with open(temp_filename, 'r', encoding='utf-8') as file:
        csv_data = file.read()

    if os.path.exists(temp_filename):
        os.remove(temp_filename)

    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="profiles.csv"'
    return response
