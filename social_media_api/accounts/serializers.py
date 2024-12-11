from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# Get the custom user model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # Add password fields explicitly using CharField
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'bio', 'profile_picture', 'followers']

    def create(self, validated_data):
        # Extract and validate passwords
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords must match."})

        # Use create_user for password hashing and user creation
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        user.set_password(password)
        user.save()

        # Generate an authentication token for the user
        Token.objects.create(user=user)
        return user
