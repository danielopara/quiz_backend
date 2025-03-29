from api.quiz.service import QuizService
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_quiz(request):
    return QuizService().get_quiz(request)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def answer(request):
    return QuizService().answer_quiz(request)