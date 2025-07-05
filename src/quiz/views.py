from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Deck, FlashCard
from django.contrib.auth.decorators import login_required


def index(request):
    """Display all available decks on the dashboard"""
    decks = Deck.objects.all().order_by('-updated_at')

    # Add basic card count for each deck
    for deck in decks:
        deck.total_cards = deck.cards.count()

    context = {
        'decks': decks,
        'total_decks': decks.count()
    }
    return render(request, 'quiz/index.html', context)


def create_deck(request):
    """Handle deck creation"""
    if request.method == 'POST':
        deck_name = request.POST.get('deck_name', '').strip()
        tags = request.POST.get('tags', '').strip()

        if deck_name:
            deck = Deck.objects.create(
                deck_name=deck_name,
                tags=tags
            )
            messages.success(request, f'Deck "{deck_name}" created successfully!')
            return redirect('deck_detail', deck_id=deck.id)
        else:
            messages.error(request, 'Please provide a deck name.')

    return render(request, 'quiz/create_deck.html')


def deck_detail(request, deck_id):
    """Display deck details and cards"""
    deck = get_object_or_404(Deck, id=deck_id)
    cards = deck.cards.all().order_by('-created_at')

    context = {
        'deck': deck,
        'cards': cards,
        'total_cards': cards.count()
    }
    return render(request, 'quiz/deck_detail.html', context)

@login_required
def profile_view(request):
    return render(request, 'account/profile.html', {'user': request.user})
