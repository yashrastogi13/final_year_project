from django.shortcuts import render,redirect
from .models import Post,Like
from profiles.models import Profile,Relationship
from .forms import PostModelForm,CommentModelForm
from django.views.generic import UpdateView,DeleteView  #class based views
from django.urls import reverse_lazy    #reverse is used for function views and reverse lazy for class based views
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

@login_required
def post_comment_create_and_list_view(request):
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    
    friends = profile.get_friends()
    #getting profile of all the friends of current user
    friends_profile = []
    for person in friends:
        temp = Profile.objects.get(user=person)
        friends_profile.append(temp)

    #storing the profiles of all the relevent persons in set
    required_profiles = set()
    for person in friends_profile:
        required_profiles.add(person)
    required_profiles.add(profile)

    #separating the post which are required
    required_posts = []
    for post in qs:
        #matching profiles of post's author and required_profiles
        if post.author in required_profiles:
            required_posts.append(post)
    
    is_empty = False

    if len(required_posts) == 0:
        is_empty = True

    #post form
    p_form = PostModelForm()

    #check whether post is added or not
    post_added = False

    #comment form
    c_form = CommentModelForm()

    if 'submit_p_form' in request.POST:
        #print(request.POST)
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            #before saving we need to set the author field which we can get from profile
            instance = p_form.save(commit=False)
            instance.author = profile      #author need to be added without it we cannot save the post form
            instance.save()
            p_form = PostModelForm()
            post_added = True

    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))        #accessing value from form through request
            instance.save()
            c_form = CommentModelForm()   #reseting the form

    context = {
        'qs':required_posts,
        'profile':profile,
        'p_form':p_form,
        'c_form':c_form,
        'post_added':post_added,
        'is_empty':is_empty,
    }

    return render(request, 'posts/main.html', context)

@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

            post_obj.save()
            like.save()

    return redirect('posts:main_post_view')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:main_post_view')
    #success_url = 'posts/'

    #check for deleting post done by user
    def get_object(self, *args, **kwargs):  #get_object is provided by DeleteView class
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk = pk)

        #in case a user accesses the delete_page of post of another user
        if not obj.author.user == self.request.user:
            messages.warning(self.request, "You need to be the author of the post in order to delete it")
        return obj

class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main_post_view')

    def form_valid(self,form):
        profile = Profile.objects.get(user= self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            #in case a user access the update_page of post of another user
            form.add_error(None, "You need to be the author of the post in order to update it")  
            return super().form_invalid(form)


