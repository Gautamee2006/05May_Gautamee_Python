from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from .models import InfluencerProfile

from .forms import InfluencerProfileForm


# --------------------------------------------------
# PROFILE VIEW
# --------------------------------------------------

@login_required
def profile_view(request):

    profile, created = InfluencerProfile.objects.get_or_create(

        user=request.user,

        defaults={
            'display_name': request.user.username
        }
    )


    return render(

        request,

        'influencer_app/profile.html',

        {
            'profile': profile
        }
    )


# --------------------------------------------------
# EDIT PROFILE VIEW
# --------------------------------------------------

@login_required
def edit_profile_view(request):

    profile, created = InfluencerProfile.objects.get_or_create(

        user=request.user,

        defaults={
            'display_name': request.user.username
        }
    )


    if request.method == 'POST':

        form = InfluencerProfileForm(

            request.POST,

            request.FILES,

            instance=profile
        )


        if form.is_valid():

            form.save()

            return redirect('profile')


    else:

        form = InfluencerProfileForm(
            instance=profile
        )


    return render(

        request,

        'influencer_app/edit_profile.html',

        {
            'form': form,
            'profile': profile
        }
    )