from rest_framework import serializers
from .models import Topic, Project, Booking , ContactMessage , CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'





class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("username")
        password = attrs.get("password")
        
        
        # Authenticate user using email
        user = CustomUser.objects.filter(email=email).first()
        # # Authenticate user using email
        # user = authenticate(username=email, password=password)
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")
        # Use the default token creation process
        data = super().validate(attrs)
        print(user)
        data["email"] = user.email  # Add email to the token payload
        data["username"] = user.username  # Add username to the token payload
        data['joined'] = user.date_joined
        return data
    
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email
        token["username"] = user.username

        return token



class RegisterSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=150)
    # email = serializers.EmailField()
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
    
    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken. Please choose a different one.")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered. Please use a different email.")
        return value

    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        return value    
    def create(self, validated_data):
        # Use the create_user method to ensure proper password hashing
        return CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )