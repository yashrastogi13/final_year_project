from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile,Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView,DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Post
# Create your views here.

@login_required
def get_users_posts(request, *args, **kwargs):
    profile = Profile.objects.get(user=request.user)
    users_posts = Post.objects.filter(author = profile)
    is_empty = False

    if len(users_posts) == 0:
        is_empty = True

    context = {
        'posts':users_posts,
        'is_empty':is_empty,
    }

    return render(request, 'profiles/timeline.html', context)

@login_required
def my_friends(request):
    profile = Profile.objects.get(user = request.user)
    friends = profile.get_friends()
    friends_profile = []
    for friend in friends:
        temp = Profile.objects.get(user = friend)
        friends_profile.append(temp)

    is_empty = False
    if len(friends_profile) == 0:
        is_empty =True

    context = {
        'friends':friends_profile,
        'is_empty':is_empty,
    }

    return render(request, 'profiles/friends_list.html', context)

@login_required
def my_profile_view(request):
    #getting the profile of the user who is logged in
    profile = Profile.objects.get(user = request.user)

    #Creating form from the model 
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    
    #this act as a flag which changes to true on a certain condition
    confirm = False

    if request.method == "POST":
        if form.is_valid():
            full_name = form.first_name + " " + form.last_name
            form.full_name = full_name
            form.save()
            confirm = True
    
    context = {
        'profile':profile,
        'form': form,
        'confirm':confirm,
    }

    return render(request, 'profiles/myprofile.html', context)

@login_required
def invite_received(request):
    #geting the profile of the logged_in user
    profile = Profile.objects.get(user = request.user)

    #using the extended behaviour of the objects
    qs = Relationship.objects.invitations_received(profile)

    results = list(map(lambda x: x.sender, qs))  #get sender from qs and insert it into result
    is_empty = False

    if len(results) == 0:
        is_empty = True

    context = {
        'qs':results,
        'is_empty':is_empty,
    }

    return render(request, 'profiles/my_invites.html', context)

@login_required
def accept_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')       
        sender = Profile.objects.get(pk=pk)         #getting sender from primary key
        receiver = Profile.objects.get(user=request.user)    
        rel = get_object_or_404(Relationship,sender=sender,receiver=receiver) # another way of getting the object
        if rel.status == 'send':
            rel.status = "accepted"
            rel.save()
            sender.friends.add(receiver.user)
            receiver.friends.add(sender.user)
            sender.save()
            receiver.save()
    return redirect('profiles:my_invites_view')
         
@login_required
def reject_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)         #getting sender from primary key
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship,sender=sender,receiver=receiver)
        rel.delete()
    return redirect('profiles:my_invites_view')

@login_required
def invite_profile_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)
    is_empty = False

    if len(qs) == 0:
        is_empty = True
    
    profile = Profile.objects.get(user = user)
    rel_1 = Relationship.objects.filter(receiver=profile) 
    rel_receiver = set()

    rel_2 = Relationship.objects.filter(sender=profile)
    rel_sender = set()

    for item in rel_1:
        rel_receiver.add(item.sender.user)   #adding sender to the set

    for item in rel_2:
        rel_sender.add(item.receiver.user)   #adding receiver to the set
    
    final_rel = rel_receiver.union(rel_sender)

    if len(qs) == len(final_rel):            #checking if length of both are equal then 
        is_empty = True                      #there is no user left to send the request

    context = {
        'qs':qs,
        'is_empty':is_empty,
        'rel_receiver':final_rel,
    }

    return render(request, 'profiles/invite_profile_list.html', context)

"""
def profile_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)
    context = {'qs':qs}
    return render(request, 'profiles/profile_list.html', context)
"""

#corresponding class based view to above function view
class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = "qs"                        #this refers to the context  

    #get_query_set is used to overrides the default query_set
    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    #this is used to add additional data to context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        context["profile"] = profile
        rel_r = Relationship.objects.filter(sender=profile)    #it store relationship we send to other user
        rel_s = Relationship.objects.filter(receiver=profile)  #it store relationship send by other user to our profile
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)

        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context["is_empty"] = False

        if len(self.get_queryset()) == 0:
            context["is_empty"] = True
        
        return context

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.html'
    
    #overriding the default get_object to get some extra functionality
    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile
    
    #overriding default get_context_data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        context["profile"] = profile
        rel_r = Relationship.objects.filter(sender=profile)    #it store relationship we send to other user
        rel_s = Relationship.objects.filter(receiver=profile)  #it store relationship send by other user to our profile
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context["posts"] = self.get_object().get_authors_post()
        context["len_posts"] = True if len(self.get_object().get_authors_post()) > 0 else False
        return context




# function for changing the state from (add to friends)-> (waiting for approval)
@login_required
def send_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')       #fetching profile_pk from form in profile_list.html 
        user = request.user                       
        sender = Profile.objects.get(user=user)   
        receiver = Profile.objects.get(pk=pk)     #getting receiver from pk of the profile object
        
        #creating a new relatioship b/w sender and receiver
        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send') 

        return redirect(request.META.get('HTTP_REFERER'))  # redirect to the same page
    
    #when the request is not POST request
    return redirect('profiles:my_profile_view')  

# function for removing the friends from the friend list 
@login_required
def remove_from_friends(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')        
        user = request.user                       
        sender = Profile.objects.get(user=user)   
        receiver = Profile.objects.get(pk=pk)

        #complex lookup using Q 
        #since we dont know who send the request to whom so we need to search both ways
        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender)))
        
        rel.delete()                                 
        return redirect(request.META.get('HTTP_REFERER'))  # redirect to the same page
    
    #when the request is not POST request
    return redirect('profiles:my_profile_view') 
        

