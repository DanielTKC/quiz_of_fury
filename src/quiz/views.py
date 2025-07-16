from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import Deck, FlashCard
from .services.scheduler import Scheduler
from django.contrib.auth.decorators import login_required


def index(request):
    """Display all available decks on the dashboard"""
    decks = Deck.objects.filter(owner=request.user).order_by('-updated_at')

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
                tags=tags,
                owner=request.user  # Set the owner to the current user
            )
            messages.success(request, f'Deck "{deck_name}" created successfully!')
            return redirect('deck_detail', deck_id=deck.id)
        else:
            messages.error(request, 'Please provide a deck name.')

    return render(request, 'quiz/create_deck.html')


def deck_detail(request, deck_id):
    """Display deck details and cards"""
    deck = get_object_or_404(Deck, id=deck_id, owner=request.user)
    cards = deck.cards.all().order_by('-created_at')

    context = {
        'deck': deck,
        'cards': cards,
        'total_cards': cards.count()
    }
    return render(request, 'quiz/deck_detail.html', context)


def add_card(request, deck_id):
    """Add a new card of furry to the deck"""
    deck = get_object_or_404(Deck, id=deck_id, owner=request.user)

    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        answer = request.POST.get('answer', '').strip()
        tags = request.POST.get('tags', '').strip()

        if question and answer:
            FlashCard.objects.create(
                deck=deck,
                question=question,
                answer=answer,
                tags=tags,
                difficulty=3.0
            )
            messages.success(request, 'Card added!')
            return redirect('deck_detail', deck_id=deck.id)
        else:
            messages.error(request, 'You have to provide a question AND and answer.')

    context = {
        'deck': deck
    }
    return render(request, 'quiz/add_card.html', context)


def study_deck(request, deck_id):
    """Start or continue studying a  deck"""
    deck = get_object_or_404(Deck, id=deck_id, owner=request.user)
    cards = deck.cards.all()

    if not cards.exists():
        messages.error(request, 'This deck has no fury to study!')
        return redirect('deck_detail', deck_id=deck.id)

    # Get current card index from session
    current_card_index = request.session.get(f'study_deck_{deck_id}_index', 0)

    # If all cards are studied, reset to beginning
    if current_card_index >= cards.count():
        current_card_index = 0
        request.session[f'study_deck_{deck_id}_index'] = current_card_index
        messages.success(request, 'All cards complete, starting over.')

    card = cards[current_card_index]
    cards_studied = current_card_index
    total_cards = cards.count()
    cards_remaining = total_cards - current_card_index - 1

    # Session data for template
    session_data = {
        'cards_studied': cards_studied,
        'total_due': total_cards,
    }

    context = {
        'deck': deck,
        'card': card,
        'session_data': session_data,
        'cards_remaining': cards_remaining,
    }

    return render(request, 'quiz/study_card.html', context)


@require_POST
@csrf_exempt
def rate_card(request, deck_id, card_id):
    """Handle card rating and advance to next card"""
    try:
        # Get the deck and card
        deck = get_object_or_404(Deck, id=deck_id, owner=request.user)
        card = get_object_or_404(FlashCard, id=card_id, deck=deck)


        # Parse the JSON data
        data = json.loads(request.body)
        rating = data.get('rating')


        # make sure the rating is valid
        if not rating or not (1 <= int(rating) <= 5):
            return JsonResponse({'error': 'Invalid rating'}, status=400)

        # Update card difficulty based on rating
        card.difficulty = float(rating)

        # Use scheduler to update card intervals
        scheduler = Scheduler()
        scheduler.modify_card(card)
        card.save()

        # Advance to next card in session
        current_index = request.session.get(f'study_deck_{deck_id}_index', 0)
        cards_count = deck.cards.count()

        if current_index + 1 >= cards_count:
            # Session complete
            request.session[f'study_deck_{deck_id}_index'] = 0
            return JsonResponse({
                'success': True,
                'session_complete': True,
                'message': 'Great job! You\'ve completed all cards in this deck.You are a Fury Master.'
            })
        else:
            # Move to next card
            request.session[f'study_deck_{deck_id}_index'] = current_index + 1
            return JsonResponse({
                'success': True,
                'session_complete': False,

                'next_card_index': current_index + 1
            })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def profile_view(request):
    return render(request, 'account/profile.html', {'user': request.user})


@login_required
def share_deck(request, deck_id):
    """Copies a deck and all its cards, assigning the copy to the current user."""
    # Get the deck or 404
    original_deck = get_object_or_404(Deck, id=deck_id)

    # Create a new deck for the current user
    new_deck = Deck.objects.create(
        deck_name=f"{original_deck.deck_name} (Copy)",
        tags=original_deck.tags,
        owner=request.user,
    )

    # Copy each FlashCard (all fields except pk/id and deck)
    for card in original_deck.cards.all():
        FlashCard.objects.create(
            deck=new_deck,
            question=card.question,
            answer=card.answer,
            tags=card.tags,
            disabled=card.disabled,
        )

    messages.success(
        request,
        f'Shared deck "{original_deck.deck_name}" to your account!'
    )
    return redirect('deck_detail', deck_id=new_deck.id)