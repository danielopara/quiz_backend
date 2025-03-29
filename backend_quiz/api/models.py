import uuid

from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import AutoSlugField


class UserProfile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='quiz_profile',
        to_field='username',
        db_column='user_username'
    )
    slug = AutoSlugField(populate_from='user__username', editable=False, unique=True)
    games_amount = models.PositiveIntegerField(default=0)
    games_won= models.PositiveIntegerField(default=0)
    games_lost= models.PositiveIntegerField(default=0)
    
    
    def __str__(self) -> str:
        return f"{self.user.username}"
    
class Quiz(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    question_number = models.PositiveIntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D','D')])
    
    def __str__(self):
        return self.question
