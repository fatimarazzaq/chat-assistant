from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


# Create your views here.


def user_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use!")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Your account has been created successfully! You can now log in.")
        return redirect("login")

    return render(request, "accounts/signup.html")



def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect("chat_home")  # Change "home" to the name of your homepage URL pattern
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "accounts/login.html")

def user_profile(request):
    return render(request, "accounts/profile.html")

def user_edit_profile(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        bio = request.POST.get("bio")
        
        # Update user profile
        user = request.user
        profile = user.userprofile
        profile.full_name = full_name
        profile.bio = bio
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        # Save changes
        user.email = email
        user.save()
        profile.save()
        
        return redirect('user-profile')
        
    return render(request, "accounts/edit-profile.html")

def user_logout(request):
    logout(request)
    return redirect('login')

# API Views
class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Login successful'
        })

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'message': 'Logout successful'
            })
        except Exception:
            return Response({
                'message': 'Logout successful'
            })

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            return Response({
                'access': str(token.access_token)
            })
        except Exception:
            return Response({
                'error': 'Invalid refresh token'
            }, status=status.HTTP_401_UNAUTHORIZED)