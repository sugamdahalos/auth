from rest_framework import serializers
from .models import User, UserProfile

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """User serializer for creating and updating users."""
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'is_active', 'is_staff']


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer for creating and updating user profiles."""
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'website', 'social_media_link']

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.website = validated_data.get('website', instance.website)
        instance.social_media_link = validated_data.get('social_media_link', instance.social_media_link)
        instance.save()
        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True)  # Include password field for registration

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        # Extract and hash the password
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
