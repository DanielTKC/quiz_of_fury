from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Deck(models.Model):
    id = models.AutoField(primary_key=True)
    deck_name = models.CharField(max_length=200)
    tags = models.CharField(max_length=300, blank=True)

    # TODO: Not sure how auth works yet, this should not be a string field
    user = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)