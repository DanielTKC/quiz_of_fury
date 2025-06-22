from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Deck(models.Model):
    id = models.AutoField(primary_key=True)
    # User ownership disabled for now
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    deck_name = models.CharField(max_length=200)
    tags = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FlashCard(models.Model):
    # Storage fields - basic card information
    id = models.AutoField(primary_key=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    question = models.TextField()
    answer = models.TextField()
    tags = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    difficulty = models.FloatField(
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    disabled = models.BooleanField(default=False)

    # Spaced repitition algorithm fields
    consecutive_correct = models.IntegerField(default=0)
    ease_factor = models.FloatField(default=2.5)
    interval = models.IntegerField(default=0)
    next_review = models.DateTimeField(null=True, blank=True)

