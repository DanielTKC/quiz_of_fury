from django.core.management.base import BaseCommand

from django.utils import timezone
from datetime import timedelta
from quiz.models import Deck, FlashCard


class Command(BaseCommand):
    def handle(self, *args, **options):


        FlashCard.objects.all().delete()
        Deck.objects.all().delete()


        spanish_deck = Deck.objects.create(
            deck_name="Spanish Vocabulary - Beginner",
            tags="Spanish, Language, Beginner"
        )

        spanish_cards = [

            ("Hola", "Hello"),
            ("Adiós", "Goodbye"),
            ("Por favor", "Please"),
            ("Gracias", "Thank you"),
            ("¿Cómo estás?", "How are you?"),
            ("Muy bien", "Very well"),
            ("¿Cómo te llamas?", "What is your name?"),
            ("Me llamo...", "My name is..."),
            ("¿Cuántos años tienes?", "How old are you?"),
            ("Tengo ... años", "I am ... years old"),
            ("¿De dónde eres?", "Where are you from?"),
            ("Soy de...", "I am from..."),
            ("No entiendo", "I don't understand"),
            ("¿Hablas inglés?", "Do you speak English?"),
            ("Un poco", "A little bit "),
        ]

        for i, (question, answer) in enumerate(spanish_cards):
            # Mix up review times for demo purposes
            if i < 5:  # First 5 cards are due now
                next_review = timezone.now() - timedelta(hours=1)
                consecutive = 0
                interval = 1
            elif i < 10:  # Next 5 cards are due soon
                next_review = timezone.now() + timedelta(hours=2)
                consecutive = 1
                interval = 2
            else:  # Rest are due later
                next_review = timezone.now() + timedelta(days=3)
                consecutive = 2
                interval = 4

            FlashCard.objects.create(
                deck=spanish_deck,
                question=question,
                answer=answer,
                tags="vocabulary",
                difficulty=3.0,
                consecutive_correct=consecutive,
                interval=interval,
                next_review=next_review

            )

        # Create Biology Deck

        biology_deck = Deck.objects.create(
            deck_name="Biology 102 - Cell Structure",
            tags="Biology, Science, College"
        )


        biology_cards = [
            ("What is the powerhouse of the cell?", "Mitochondria"),
            ("What controls what enters and leaves the cell?", "Cell membrane"),
            ("Where is genetic material stored in a cell?", "Nucleus"),
            ("What produces proteins in the cell?", "Ribosomes"),
            ("What is the jelly-like substance inside the cell?", "Cytoplasm"),
            ("What is the function of the endoplasmic reticulum?", "Protein and lipid synthesis"),
            ("What organelle is responsible for photosynthesis?", "Chloroplasts"),
            ("What structure provides support and shape to plant cells?", "Cell wall"),
            ("What is the function of lysosomes?", "Digestion and waste removal"),
            ("What is the role of the Golgi apparatus?", "Modifying, sorting, and packaging proteins"),

        ]

        for i, (question, answer) in enumerate(biology_cards):
            # Some cards due, some not
            if i < 3:
                next_review = timezone.now() - timedelta(minutes=30)
                consecutive = 0
                interval = 1
            else:
                next_review = timezone.now() + timedelta(days=1)
                consecutive = 1
                interval = 3

            FlashCard.objects.create(
                deck=biology_deck,
                question=question,
                answer=answer,
                tags="cell biology",
                difficulty=4.0,
                consecutive_correct=consecutive,
                interval=interval,
                next_review=next_review
            )

        # Create Math Deck
        math_deck = Deck.objects.create(
            deck_name="Algebra - Basic Formulas",
            tags="Math, Algebra, Formulas"
        )

        math_cards = [
            ("What is 2 + 2?", "4"),
            ("What is the formula for the area of a rectangle?", "Length x Width"),
            ("What is the Pythagorean theorem?", "a² + b² = c²"),
            ("What is the formula for the circumference of a circle?", "2πr"),
            ("What is the formula for the area of a circle?", "πr²"),

        ]

        for i, (question, answer) in enumerate(math_cards):
            FlashCard.objects.create(
                deck=math_deck,
                question=question,
                answer=answer,
                tags="formulas",
                difficulty=4.0,
                consecutive_correct=1,
                interval=2,
                next_review=timezone.now() + timedelta(days=2)
            )
