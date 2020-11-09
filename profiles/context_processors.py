from .models import Profile,Relationship
import json

def profile_dp(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        pic = profile_obj.avatar
        return {'picture':pic}
    return {}

def invitation_received_no(request):
    if request.user.is_authenticated:                
        profile_obj = Profile.objects.get(user=request.user)
        #invitation received require a receiver
        qs_count = Relationship.objects.invitations_received(profile_obj).count()
        return {'invites_no':qs_count}
    return {} 

def friends_no(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        count = profile_obj.get_friends_no()
        return {'friend_count':count}
    return {}

def search_profiles(request):
    if request.user.is_authenticated:
        context = {}
        context["qs_json"] = json.dumps(list(Profile.objects.values()), default=str)
        return context
    else:
        return {}
        
# class SearchListView(ListView):
#     model = Profile
#     template_name = "main/navbar.html"
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["qs_json"] = json.dumps(list(Profile.objects.values()), default=str)
#         print(context,"Hello")
#         return context





