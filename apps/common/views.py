from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer, UserLoginSerializer
from django.contrib.auth.models import User
from apps.common.utils import get_tokens_for_user

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response(
            {"user": UserSerializer(user, context=self.get_serializer_context()).data,
             "token": token},
            status=status.HTTP_201_CREATED,
        )

class UserLoginView(ModelViewSet):
    serializer_class = UserLoginSerializer
    def get_queryset(self):
        return []
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user:
                token = get_tokens_for_user(user)
                return Response({"token": token})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
