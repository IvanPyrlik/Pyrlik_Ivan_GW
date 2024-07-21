from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.views import RegisterView, UserUpdateView, get_key_user, pay_sub, repeat_key

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('update_user/', UserUpdateView.as_view(), name='update_user'),
    path('confirm_phone/', get_key_user, name='confirm_phone'),
    path('pay_sub/', pay_sub, name='pay_sub'),
    path('repeat_key/', repeat_key, name='repeat_key'),
]
