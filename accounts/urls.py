from django.urls import path 
from . import views
from django.contrib.auth.views import LogoutView
app_name = "accounts"
urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('changePassword/', views.change_password, name='changePassword'),
]