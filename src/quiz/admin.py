from django.contrib import admin
from quiz.models import FlashCard, Deck, Profile

class FlashCardInline(admin.TabularInline):
    model = FlashCard
    extra = 1
    fields = ('question', 'answer', 'difficulty', 'disabled', 'next_review')
    show_change_link = True

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('deck_name', 'created_at', 'updated_at')
    search_fields = ('deck_name', 'tags')
    inlines = [FlashCardInline]

@admin.register(FlashCard)
class FlashCardAdmin(admin.ModelAdmin):
    list_display = ('question', 'deck', 'difficulty', 'next_review')
    list_filter = ('disabled', 'deck')
    search_fields = ('question', 'answer', 'tags')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'study_streak')
    search_fields = ('user__username',)