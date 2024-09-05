from django.contrib import admin
from django.urls import path, include
from users.views import SignupView, LoginView, UserSearchView, ListFriendsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friends/', ListFriendsView.as_view(), name='friends_list'),
]

