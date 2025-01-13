from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, ContactView ,CustomTokenObtainPairView ,CheckUsernameView
urlpatterns = [
    # path('login/', obtain_auth_token, name='login'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh tokens
    path('register/',RegisterView.as_view(), name='register'),
    path('contact/' , ContactView.as_view(), name='contact'),
    path('check-username/' , CheckUsernameView.as_view(), name='check-username'),
]
