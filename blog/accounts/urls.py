from django.urls import path
from .views import follow_user_view, unfollow_user_view, FollowerListView, FollowingListView


urlpatterns = [
    path('follow/<int:pk>/', follow_user_view, name='follow-user'),
    path('unfollow/<int:pk>/', unfollow_user_view, name='unfollow-user'),
    path('followers/', FollowerListView.as_view(), name='follower_list'),
    path('following/', FollowingListView.as_view(), name='following_list'),
]
