from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    """User Manager for the custom User model"""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
        
class User(AbstractBaseUser):
    """Custom User model with email as the unique identifier"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class UserProfile(models.Model):
            """User profile of each user in the system"""
            user = models.OneToOneField(User, on_delete=models.CASCADE)
            bio = models.TextField(blank=True)
            profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
            website = models.URLField(blank=True)
            social_media_link = models.CharField(max_length=200, blank=True)

            def save(self, *args, **kwargs):
                # Check if a new profile picture has been uploaded
                if self.pk:
                    try:
                        old_profile = UserProfile.objects.get(pk=self.pk)
                        if old_profile.profile_picture != self.profile_picture:
                            if old_profile.profile_picture:
                                if os.path.isfile(old_profile.profile_picture.path):
                                    os.remove(old_profile.profile_picture.path)
                    except UserProfile.DoesNotExist:
                        pass

                super().save(*args, **kwargs)

