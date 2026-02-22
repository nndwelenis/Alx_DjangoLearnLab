from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from rest_framework.permissions import IsAuthenticated

# Create your views here.

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        token = Token.objects.get(user=user)

        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
    

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    

User = get_user_model()


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = User.objects.filter(id=user_id).first()
        if target_user is None:
            return Response({"detail": "User not found."}, status=404)

        if target_user == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=400)

        request.user.following.add(target_user)

        return Response(
            {"detail": f"You are now following {target_user.username}."},
            status=200
        )


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = User.objects.filter(id=user_id).first()
        if target_user is None:
            return Response({"detail": "User not found."}, status=404)

        if target_user == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=400)

        request.user.following.remove(target_user)

        return Response(
            {"detail": f"You have unfollowed {target_user.username}."},
            status=200
        )