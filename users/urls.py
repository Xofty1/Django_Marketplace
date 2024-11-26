from django.urls import path, reverse_lazy

from django.contrib.auth.views import PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

from users.views import logout_user, LoginUser, RegisterUser, ProfileUser, \
    home_view, UserPasswordChange, UserPasswordResetConfirmView, \
    increase_coins, coins_page

app_name = 'users'

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/', ProfileUser.as_view(), name='profile'),
    path('home/', home_view, name='home'),
    path('password_change/', UserPasswordChange.as_view(),
         name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(
        template_name="users/password_change_done.html"),
         name='password_change_done'),

    path('password-reset/',
         PasswordResetView.as_view(
             template_name="users/password_reset_form.html",
             email_template_name="users/password_reset_email.html",
             success_url=reverse_lazy("users:password_reset_done")),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(
             template_name="users/password_reset_done.html"),
         name='password_reset_done'),

    path('password-reset/<uidb64>/<token>/',
         UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(
             template_name="users/password_reset_complete.html"),
         name='password_reset_complete'),

    path('increase-coins/', increase_coins, name='increase_coins'),
    path('coins/', coins_page, name='coins_page'),
]
