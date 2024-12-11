from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()
serializers.CharField()
get_user_model().objects.create_user
class UserSerializer(serializers.ModelSerializer):
    # Define password explicitly as it needs special handling
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'bio', 'profile_picture', 'followers']

    def create(self, validated_data):
        # Ensure passwords match
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords must match."})

        # Create the user
        user = User.objects.create_user(**validated_data)
        
        # Create an authentication token for the user
        Token.objects.create(user=user)
        return user
