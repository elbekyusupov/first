from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from account.models import User
from chatrest.serializers import UserSerializer


def index(request):
    return render(request, 'rest_index.html')

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer