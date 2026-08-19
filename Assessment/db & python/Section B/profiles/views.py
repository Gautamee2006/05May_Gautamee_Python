from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm

def create_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profiles')
    else:
        form = UserProfileForm()
    return render(request, 'create_profile.html', {'form': form})

def profiles(request):
    all_profiles = UserProfile.objects.all()
    context = {
        'profiles': all_profiles
    }
    return render(request, 'profiles.html', context)

