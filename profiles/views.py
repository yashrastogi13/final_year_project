from django.shortcuts import render
from .models import Profile
from .forms import ProfileModelForm
# Create your views here.

def my_profile_view(request):
    #getting the profile of the user who is logged in
    profile = Profile.objects.get(user = request.user)

    #Creating form from the model 
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    
    #this act as a flag which changes to true on a certain condition
    confirm = False

    context = {
        'profile':profile,
        'form': form,
        'confirm':confirm,
    }

    return render(request, 'profiles/myprofile.html', context)

