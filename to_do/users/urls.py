from django.urls import path
from users.views import register, login_view, UserProfileView, UserLogoutView, UserVerifyEmailView

app_name = "users"

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('verify/<str:email>/<uuid:key>/', UserVerifyEmailView.as_view(), name='verify'),
]
