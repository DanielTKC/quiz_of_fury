from django.db import models

class Deck(models.Model):
    id = models.AutoField(primary_key=True)
    # User ownership disabled for now
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    deck_name = models.CharField(max_length=200)
    tags = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)