from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
class Review(models.Model):
    place_name = models.CharField(max_length=255)
    review_text = models.TextField()
    sentiment = models.CharField(max_length=20)
    sentiment_score = models.FloatField()

    def __str__(self):
        return f"{self.place_name}: {self.sentiment} ({self.sentiment_score})"
# class CustomUser(AbstractUser):
#     # Add any additional fields you want for your user model
#     bio = models.TextField(blank=True, null=True)