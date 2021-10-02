from django.urls import path 
from . import views
from django.contrib.auth.views import LogoutView


app_name = "core"



urlpatterns = [
    path('', views.Landing , name='landing'),
    path('home/', views.PostListView.as_view() , name='home'),
    path('myProfile/', views.myProfilePage , name='profile'),
    path('editProfile/<int:pk>/', views.EditProfilePage.as_view() , name='editProfile'),
    path('profile/<str:username>/', views.othersProfilePage , name='othersProfile'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('postDetail/<int:pk>/', views.PostDetailView.as_view(), name='postDetail'),
    path('post/<int:pk>/like/', views.LikeToggle.as_view(), name='like'),
    path('profile/<int:pk>/follow/', views.FollowToggle.as_view(), name='follow'),
    path('search/', views.UserSearch.as_view(), name='profileSearch'),
    path('profile/<int:pk>/followersList/', views.FollowersList.as_view(), name='followersList'),
    path('profile/<int:pk>/followingList/', views.FollowingList.as_view(), name='followingList'),
    path('postDelete/,<int:pk>/', views.PostDeleteView.as_view(), name='postDelete'),
    path('postUpdate/<int:pk>/', views.PostUpdateView.as_view(), name='postUpdate'),
    path('profile/verify-email/<int:pk>/', views.VerifyEmail.as_view(), name='verifyEmail'),
    path('email-verification/<int:id>/<str:token>/', views.EmailVerification.as_view())
    # path('home/', views.home , name='home'),
]