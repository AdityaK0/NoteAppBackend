from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import CustomUser  # Use CustomUser instead of default CustomUser
from .serializers import CustomUserSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from notes.models import Notes

# Authentication Home Route
@api_view(["GET"])
def auth_home(request):
    return Response({"message": "Welcome to the authentication API!"})


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }



@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    fullname = request.data.get('fullname')
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not all([fullname, username, email, password]):
        return Response({"error": "Please enter valid details to create an account"},
                        status=status.HTTP_400_BAD_REQUEST)
    
    

    if CustomUser.objects.filter(username=username).exists():
        print("already exists")
        return Response({"error": "Username already exists"},
                        status=status.HTTP_400_BAD_REQUEST)
    if CustomUser.objects.filter(email=email).exists():
        return Response({"error":"Email already registered"},
                        status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser.objects.create(username=username, email=email, fullname=fullname)
    user.set_password(password)  
    user.save()

    token = get_tokens_for_user(user)

    return Response({"message": "CustomUser registered successfully!",
                     "user":CustomUserSerializer(user).data,
                     "token":token
                     }, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username_or_email = request.data.get("username")  # Can be username or email
    password = request.data.get("password")

    if not username_or_email or not password:
        return Response({"error": "Username or email and password are required"},
                        status=status.HTTP_400_BAD_REQUEST)
    
   
    user = None
    if '@' in username_or_email:  
        try:
            user = CustomUser.objects.get(email=username_or_email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            user = CustomUser.objects.get(username=username_or_email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    authenticated_user = authenticate(request, username=user.username, password=password)  

    if authenticated_user is not None:
        token = get_tokens_for_user(authenticated_user)  
        return Response({
            "message": "Login successful!",
            "user": CustomUserSerializer(authenticated_user).data,
            "token": token
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get("refresh")
        access_token = request.data.get("access")
        if not refresh_token or not access_token:
            return Response({
                "error":"Refresh token and Access token is required"
            },status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken(refresh_token)
        refresh.blacklist()

        access = RefreshToken(access_token)
        access.blacklist() 

        return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK) 
    except Exception as e:
         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request):
    try:
        if request.user:
            # if cache_user = 
            serializer = CustomUserSerializer(request.user)
            excluded_data = {}
            for key,val in serializer.data.items():
                if key in ["password" , "is_superuser" , "first_name" , "last_name"]:
                    pass
                else:
                    excluded_data[key] = val
            total_notes = Notes.objects.filter(user = excluded_data["id"]).count()
            excluded_data["total_notes"] =  total_notes 

            return Response(excluded_data,status=status.HTTP_200_OK)
        else:
            return Response({"error":"User is not available"},status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"error":f" Error = {e}"},status=status.HTTP_400_BAD_REQUEST)



class protectedView(APIView):
    print("called")
    permission_classes = [IsAuthenticated]

    def get(self,request):
        return Response({"message":f"Hello  {request.user.username}","username":request.user.username,"id":request.user.username})