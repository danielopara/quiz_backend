from api.user.service import UserService
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def register(request):
    return UserService().create_user(request)

@api_view(['GET'])
def get_user(request):
    return UserService().get_user(request)

@api_view(["POST"])
def login(request):
    return UserService().login(request)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_auth_user(request):
    return UserService().get_authorized_user(request)