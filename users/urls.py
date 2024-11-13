from django.urls import path
from users.views import login_user, logout_user, LoginUser, register

app_name = 'users'

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
]
