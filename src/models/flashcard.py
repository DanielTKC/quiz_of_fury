from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from deck import Deck

class FlashCard(models.Model):
    # Storage fields - basic card information
    id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    tags = models.CharField(max_length=300, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    difficulty = models.FloatField(
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    disabled = models.BooleanField(default=False)

    # Spaced repitition algorithm fields
    consecutive_correct = models.IntegerField(default=0)
    ease_factor = models.FloatField(default=2.5)
    interval = models.IntegerField
    next_review = models.DateTimeField(null=True, blank=True)

    # Deck ownership - many-to-one relationship
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE) #if the containing deck is deleted, delete all cards