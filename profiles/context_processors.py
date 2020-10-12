from .models import Profile,Relationship
 
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



