from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
)

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Following


class FollowerListView(ListView):
    model = Following
    template_name = 'accounts/followers_list.html'
    context_object_name = 'followers'
    paginate_by = 5

    def get_queryset(self):
        queryset = Following.objects.all().filter(target=self.request.user)
        return queryset

class FollowingListView(ListView):
    model = Following
    template_name = 'accounts/following_list.html'
    context_object_name = 'following'
    paginate_by = 5

    def get_queryset(self):
        queryset = Following.objects.all().filter(follower=self.request.user)
        return queryset



def follow_user_view(request, pk):
    if request.method == "POST":
        user_to_follow = get_object_or_404(User, id=pk)
        user1 = request.user
        new_link = Following.objects.create(target=user_to_follow, follower=user1)
        new_link.save()
        return redirect('user-posts', user_to_follow)
    else:
        return redirect('blog-home')

def unfollow_user_view(request, pk):
    if request.method == "POST":
        user_to_follow = get_object_or_404(User, id=pk)
        user1 = request.user
        Following.objects.filter(target=user_to_follow.id, follower=user1.id).delete()
        return redirect('user-posts', user_to_follow)
    else:
        return redirect('blog-home')


def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form':form})

@login_required
def profile(request):
    context = {}
    return render(request, 'accounts/profile.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'accounts/profile.html', context)
