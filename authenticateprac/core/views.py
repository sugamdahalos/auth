from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response(f"Hello, !")
        # Create an instance of the JWTAuthentication class
        
        # jwt_authentication = JWTAuthentication()

        # try:
        #     # Authenticate the request using JWT
        #     auth_result = jwt_authentication.authenticate(request)

        #     # Check if the user is authenticated
        #     if auth_result is not None:
        #         # Return the response with the authenticated user
        #         user, _ = auth_result
        #         return Response(f"Hello, {user.username}!")
        #     else:
        #         # Return an error response if the user is not authenticated
        #         return Response("Unauthorized", status=401)
        # except AuthenticationFailed:
        #     # Return an error response if the authentication fails
        #     return Response("Authentication Failed", status=401)
        #     # Return an error response if the user is not authenticated
        #     return Response("Unauthorized", status=401)