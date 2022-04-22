from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
    path("<str:username>/",views.ProfileDetailView.as_view(),name='detail'),
    path("edit/<str:usernames>/",views.EditProfileView.as_view(),name='editprofile'),
    path("<str:username>/follow/",views.FollowView.as_view(),name='follow'),
]