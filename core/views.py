from django.shortcuts import render
from django.db import IntegrityError
# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Topic, Project, Booking , ContactMessage , CustomUser
from .serializers import TopicSerializer, ProjectSerializer, BookingSerializer , ContactSerializer , CustomTokenObtainPairSerializer , RegisterSerializer

from rest_framework_simplejwt.views import TokenObtainPairView





class TopicViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['level', 'branch']  # Enable filtering by level and branch
class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

import logging

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    def post(self , request):
        logger.info("Register endpoint called with data: %s", request.data)
        serializer = RegisterSerializer(data = request.data)
        
        if serializer.is_valid():
            user = serializer.save()  # Uses the serializer to create a new user
            print(f"User created: {user}") 
            logger.info("User created: %s", user)
            return Response({'message': "User registered successfully" , 'user': {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }}, status=status.HTTP_201_CREATED)
        logger.error("Validation errors: %s", serializer.errors)  
        logger.exception("Error in register endpoint")  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# checking username availability
class CheckUsernameView(APIView):
    def get(self, request):
        username = request.query_params.get('username')
        if CustomUser.objects.filter(username=username).exists():
            return Response({"available": False}, status=200)
        return Response({"available": True}, status=200)


class ContactView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
             # Save the data to the database
            serializer.save()
            # Retrieve validated data from the serializer
            name = serializer.validated_data.get('name')
            email = serializer.validated_data.get('email')
            
            message = serializer.validated_data.get('message')
            print("Validated Data:", serializer.validated_data)
            print(f"Name: {name}, Email: {email}, Message: {message}")
            try:
                send_mail(
                subject=f"Contact Form Submission: {name}",
                message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=email,
                recipient_list=['alaani.hiba@gmail.com'],  # Replace with your email
                    )
                return Response({'message':"Contact message submitted successfully"}, status=status.HTTP_201_CREATED)
            except Exception as error:
                
                print(f"Error sending email: {error}")  # Debugging log
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)