from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Post, Profile, Comment
from django.views import View
from .forms import PostForm, ProfileForm, CommentForm
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.

def Landing(request):
    return render(request, 'core/landing.html') 

# @login_required
# def home(request):
#     user=request.user
#     context={'user': user}
#     return render(request, 'core/home.html', context)

@login_required
def myProfilePage(request):

    user = request.user
    posts= Post.objects.filter(author=user).order_by('-created_on')
    firstName=user.profile.fullName.split(' ')[0]

    context={
        'user': user, 
        'firstName':firstName,
        'posts':posts
        }

    return render(request, 'core/profile.html', context)

@login_required
def othersProfilePage(request, username):

    user=User.objects.get(username=username)
    posts= Post.objects.filter(author=user).order_by('-created_on')
    firstName=user.profile.fullName.split(' ')[0]
    followers = user.profile.followers.all()
    
    if request.user in followers:
        is_following=True
    else:
        is_following=False


    context={
        'user': user, 
        'firstName':firstName,
        'posts':posts,
        'is_following':is_following
        }

    return render(request, 'core/othersProfile.html', context)

class EditProfilePage(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    model=Profile
    form_class=ProfileForm
    success_url = reverse_lazy('core:profile')
    success_message="Profile changes saved!"

    def test_func(self):
        return self.request.user.profile.id == int(self.kwargs['pk'])

class PostListView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        user=request.user
        posts = Post.objects.filter(author__profile__followers__in=[user]).order_by('-created_on')
        form = PostForm()

        context = {
            'posts': posts,
            'form': form,
            'user': user
        }
        return render(request, 'core/home.html', context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        return redirect('core:home')


class PostDetailView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        post=Post.objects.get(id=self.kwargs['pk'])
        comments=Comment.objects.filter(post=post).order_by('-created_on')
        form=CommentForm()
        context={
            'post':post,
            'comments':comments,
            'form':form
        }
        return render(request, 'core/postDetail.html', context)

    def post(self, request, *args, **kwargs):
        postId=self.kwargs['pk']
        post=Post.objects.get(id=postId)
        comments=Comment.objects.filter(post=post)
        form=CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post=post
            new_comment.save()
        
        return redirect('/postDetail/'+ str(postId))

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model=Post
    form_class= PostForm
    template_name_suffix = '_updateForm'
    success_url=reverse_lazy('core:home')

    def test_func(self):
        post=Post.objects.get(id=self.kwargs['pk'])
        return self.request.user.id == post.author.id


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Post
    context_object_name='post'
    success_url=reverse_lazy('core:home')

    def test_func(self):
        post=Post.objects.get(id=self.kwargs['pk'])
        return self.request.user.id == post.author.id



class LikeToggle(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        postId=self.kwargs['pk']
        post=Post.objects.get(pk=postId)
        user=request.user
        
        liked=False
        for like in post.likes.all():
            if like==user:
                liked=True
                break

        if liked:
            post.likes.remove(user)
        
        if not liked:
            post.likes.add(user)


        next = request.POST.get('next', '/')
        return redirect(next)

class FollowToggle(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        profileId=kwargs['pk']
        profile=Profile.objects.get(id=profileId)
        
        if request.user in profile.followers.all():
            profile.followers.remove(request.user)
            request.user.profile.following.remove(profile.user)
        else:
            profile.followers.add(request.user)
            request.user.profile.following.add(profile.user)

        return redirect('/profile/{}'.format(profile.user.username))


class UserSearch(LoginRequiredMixin, View):
    def get(self,request,*args,**kwargs):
        query = self.request.GET.get('query')
        profile_list = Profile.objects.filter(Q(user__username__icontains=query))
        context={
            'profile_list': profile_list
        }
        return render(request, 'core/search.html', context)

class FollowersList(LoginRequiredMixin, View):
    def get(self,request,*args,**kwargs):
        profileId=kwargs['pk']
        profile=Profile.objects.get(id=profileId)
        context={
            'profile':profile,
        }
        return render(request, 'core/followersList.html', context)



class FollowingList(LoginRequiredMixin, View):
    def get(self,request,*args,**kwargs):
        profileId=kwargs['pk']
        profile=Profile.objects.get(id=profileId)
        context={
            'profile':profile,
        }
        return render(request, 'core/followingList.html', context)


class VerifyEmail(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profileId=kwargs['pk']
        profile=Profile.objects.get(id=profileId)
        context={
            'profile':profile
        }
        return render(request, 'core/verifyEmail.html', context)

    def post(self, request, *args, **kwargs):
        email=request.POST.get('email')
        profileId=request.user.profile.id
        profile=Profile.objects.get(id=profileId)
        token=profile.get_auth_token()


        subject = 'WeShare Account Email Verification'
        html_content = f'<h1>WeShare Account Email Verification</h1> <p>Click on this link to verify your account http://127.0.0.1:8000/email-verification/{profileId}/{token}</p>'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        msg = EmailMultiAlternatives(subject, html_content, email_from, recipient_list)
        msg.content_subtype = "html" 
        msg.send()
        messages.success(request, 'Verification Mail Sent Successfully')
        return redirect('core:profile')

class EmailVerification(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        token=kwargs['token']
        profileId=kwargs['id']
        profile=Profile.objects.get(id=profileId)
        if profile.verified:
            messages.warning(request, 'Email Already Verified')
            return redirect('core:profile')
        else:
            if profile.last_auth_token==token:
                profile.verified=True
                profile.save()
                messages.success(request, 'Email Verified Successfully')
                return redirect('core:profile')
            else:
                messages.error(request, 'Email Verification Failed')
                return redirect('core:profile')
        