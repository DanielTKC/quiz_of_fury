from quiz.models import FlashCard
from datetime import timedelta, datetime

class Scheduler:
    def modify_card(self, card):
        # Check diffiulty and adjust card repititons, interval accordingly
        if card.difficulty < 3.0:
            card.repititions = 0
            card.interval = 1
        else:
            card.repititions += 1
            if card.repititions == 1:
                card.interval = 1
            elif card.repititions == 2:
                card.interval = 6
            else:
                card.interval = int(card.interval * card.ease_factor)

        # remember that diffiulty is 5 for easy, 1 for very hard
        card.ease_factor = card.ease_factor + (0.1 - (5 - card.difficulty) * (0.08 + (5 - card.difficulty) * 0.02))
        if card.ease_factor < 1.3:
            card.ease_factor = 1.3
        card.next_review = datetime.now() + timedelta(days=card.interval)