from django.shortcuts import render
from .models import Profile
# Create your views here.

def my_profile_view(request):
    #getting the profile of the user who is logged in
    profile = Profile.objects.get(user = request.user)
    context = {
        'profile':profile,
    }

    return render(request, 'profiles/myprofile.html', context)
