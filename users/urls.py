from django.urls import path
from rest_framework_simplejwt.views import  TokenRefreshView
from .views import (
    RegisterUserView, LogoutView, UserListView, UserDetailView,
    CreateUserView, UpdateUserView, DeleteUserView,CustomTokenObtainPairView
)

urlpatterns = [
    # Authentication
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User Management
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/detail/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('users/create/', CreateUserView.as_view(), name='create-user'),
    path('users/update/<int:id>/', UpdateUserView.as_view(), name='update-user'),
    path('users/delete/<int:id>/', DeleteUserView.as_view(), name='delete-user'),
]
