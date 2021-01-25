from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from accounts.models import Following

class FeedListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    # ordering = ['publish_date']
    paginate_by = 5

    def get_queryset(self):
        followed_users = Following.objects.filter(follower=self.request.user)
        return Post.objects.filter(author__followers__in=followed_users).filter(publish='publish').order_by('-publish_date')

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-publish_date']
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(publish='publish').order_by('-publish_date')


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, username=self.kwargs.get('username'))
        context['follows_this_user'] = (Following.objects.filter(
                                                target=context['profile_user'].id,
                                                follower=self.request.user.id
                                                ).count() == 1)
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-publish_date')


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'image', 'content', 'publish']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'image', 'content','publish']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
