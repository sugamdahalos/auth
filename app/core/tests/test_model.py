from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status
from core.models import User, UserProfile
from core.serializers import UserSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

class RegisterViewTest(APITestCase):
    client = APIClient()

    def test_register_user(self):
    # test with valid data
        data = {
            "email": "newuser@example.com",
            "password": "newpass",
            "first_name": "New",
            "last_name": "User"
        }
        response = self.client.post(reverse("register"), data)
        expected = User.objects.get(email="newuser@example.com")
        serialized = UserSerializer(expected)
        self.assertEqual(response.data['user'], serialized.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test with invalid data
        data = {
            "email": "",
            "password": "newpass",
            "first_name": "New",
            "last_name": "User"
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')  # replace with your actual endpoint
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpass",
            "first_name": "Test",
            "last_name": "User",
            "is_active": True,
        }
        self.login_url = reverse('login')

    def test_user_profile_retrieval_and_update(self):
        # Register a user first
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=self.user_data['email'])
        self.assertIsNotNone(user)
        self.assertTrue(user.is_active)
        
        # Check if UserProfile is created
        user_profile = UserProfile.objects.get(user=user)
        self.assertIsNotNone(user_profile)
        print(user_profile.user)


        # Obtain the JWT token for the user
        response = self.client.post(self.login_url, self.user_data) # print the response data
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # assert that the request was successful
        token = response.data['access']

        # Set the Authorization header in the test client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Retrieve the user profile
        user_profile_url = reverse('profile')  # replace with your actual endpoint
        response = self.client.get(user_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['user']['email'], user.email)
        # print(response.data['user'])
        
        # Update the user profile
        image = SimpleUploadedFile(name='test_image.jpg', content=open('testfiles/test_image.jpg', 'rb').read(), content_type='image/jpeg')
        response = self.client.put(user_profile_url, {'profile_picture': image}, format='multipart')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('profile_picture', response.data)

        # Check if the image was added to the user's profile
        userprofile = UserProfile.objects.get(user=user)
        self.assertIsNotNone(userprofile.profile_picture)