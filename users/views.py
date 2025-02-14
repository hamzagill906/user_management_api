from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .serializers import UserSerializer, UserDetailSerializer
from .permissions import IsAdmin, IsEditor, IsViewer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


# Register New User
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user=request.user)

        if not tokens.exists():
            return Response({"message": "No active sessions to log out from."}, status=400)

        try:
            blacklisted_tokens = [BlacklistedToken(token=token) for token in tokens]
            BlacklistedToken.objects.bulk_create(blacklisted_tokens)
            tokens.delete()

            return Response({"message": "Logged out successfully from all sessions."}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
# List all users (Admin & Viewer)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsViewer]

# Retrieve single user (All roles)
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated , IsAdmin | IsEditor | IsViewer]

    def get_object(self):
        user_id = self.kwargs.get('id')  
        
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound({"error": "User not found"})

# Create a new user (Admin only)
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        serializer.save()
        return Response({"message": "User created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

# Update a user (Admin & Editor, but Editor cannot change roles)
class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsEditor]

    def update(self, request, *args, **kwargs):
        
        user_id = kwargs.get('id')
        if not user_id:
            raise NotFound({"error": "User ID is required"})

        user = self.queryset.filter(id=user_id).first()
        if not user:
            raise NotFound({"error": "User not found"})

        if request.user.role == User.EDITOR and 'role' in request.data:
            raise PermissionDenied({"error": "Editor cannot change roles"})

        request_data = request.data.copy()  
        if 'password' not in request_data:
            request_data.pop('password', None)  
        
        serializer = self.get_serializer(user, data=request_data)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(
            {"message": "User updated successfully", "data": serializer.data},
            status=status.HTTP_200_OK
        )

# Delete a user (Admin only)
class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('id')  # Get ID from URL parameter
        if not user_id:
            raise NotFound({"error": "User ID is required"})

        try:
            user = self.get_queryset().get(id=user_id)
        except User.DoesNotExist:
            raise NotFound({"error": "User not found"})

        user.delete()

        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

