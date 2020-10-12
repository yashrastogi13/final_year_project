from django.urls import path
from .views import (
    my_profile_view,
    invite_received,
    invite_profile_list_view,
    ProfileListView,
    ProfileDetailView,
    send_invitation,
    remove_from_friends,
    accept_invitation,
    reject_invitation,
    my_friends,
)

app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name='all_profiles_view'), 
    path('friends/', my_friends, name='my_friends_view'),    
    path('myprofile/', my_profile_view, name='my_profile_view'),
    path('my_invites/', invite_received, name='my_invites_view'),
    path('to_invite/', invite_profile_list_view, name='invite_profiles_view'),
    path('send_invite/', send_invitation, name='send_invite'),
    path('remove_friend/', remove_from_friends, name='remove_friend'),    
    path('<slug>/', ProfileDetailView.as_view(), name='profiles_detail_view'),
    path('my_invites/accept/', accept_invitation, name='accept_invite'),
    path('my_invites/reject/', reject_invitation, name='reject_invite'),
    

]


