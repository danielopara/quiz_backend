import random
from itertools import count

from api.models import Quiz
from api.serializers import QuizSerializer, UserProfileSerializer
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


class QuizService:
    def get_quiz(self, request):
        try:
            count = Quiz.objects.aggregate(count=Count('id'))['count']
            
            if count == 0:
                return Response({'message': 'no quiz found'}, status=status.HTTP_404_NOT_FOUND)
            
            random_index = random.randint(0, count - 1)
            quiz = Quiz.objects.all()[random_index]
            
            return Response({
                'id': quiz.id,
                'question': quiz.question,
                'option_a' : quiz.option_a,
                'option_b' : quiz.option_b,
                'option_c' : quiz.option_c,
                'option_d' : quiz.option_d,
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def answer_quiz(self, request):
        try:
            id = request.GET.get('id')
            answer = request.data.get('answer')
            
            # get user
            user = request.user_profile  
            if not user:
                return Response({'message': "no auth"}, status=401)
            
                    
            if not id:
                return Response({'message':'missing query'}, status=status.HTTP_400_BAD_REQUEST)
            
            quiz = Quiz.objects.filter(id=id).first()
            if not quiz:
                return Response({'message':'quiz not found'}, status=status.HTTP_404_NOT_FOUND)
            
            user.games_amount+=1
            if quiz.answer == answer.upper():
                user.games_won +=1
                user.save()
                return Response({"message": 'correct', 'user_profile': UserProfileSerializer(user).data}, status=status.HTTP_200_OK)
            user.games_lost +=1
            user.save()
            return Response({'message': 'wrong','correct_answer': quiz.answer, 'user_profile': UserProfileSerializer(user).data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)