from django.test import TestCase
from unittest.mock import Mock
from quiz.services.scheduler import Scheduler
from quiz.models import Deck, FlashCard
from datetime import datetime

class SchedulerTests(TestCase):
    def test_modify_card_four_difficulty_no_repititions(self):
        # Modify card properties and check if they are updated correctly
        # This test is for a difficulty of 4.0, which should result in one repetition
        # and an ease factor of 1.4, with an interval of 0 days.
        card1 = Mock()
        card1.difficulty = 4.0
        card1.repititions = 0
        card1.ease_factor = 1.4
        card1.interval = 0
        card1.next_review = None


        scheduler = Scheduler()
        scheduler.modify_card(card1)
        self.assertEqual(card1.difficulty, 4.0)
        self.assertEqual(card1.repititions, 1)
        self.assertEqual(card1.interval, 1)
        self.assertAlmostEqual(card1.ease_factor, 1.4)

    def test_modify_card_five_difficulty_no_repititions(self):
        # This test is for a difficulty of 5.0, which should result in one repetition
        # and an ease factor of 1.6 (ease factor increases when easy), with an interval of 0 days.
        card2 = Mock()
        card2.difficulty = 5.0
        card2.repititions = 0
        card2.ease_factor = 1.5
        card2.interval = 0
        card2.next_review = None

        scheduler = Scheduler()
        scheduler.modify_card(card2)
        self.assertEqual(card2.difficulty, 5.0)
        self.assertEqual(card2.repititions, 1)
        self.assertEqual(card2.interval, 1)
        self.assertAlmostEqual(card2.ease_factor, 1.6)

    def test_modify_card_one_difficulty_no_repititions(self):
        # This test is for a difficulty of 1.0, which should result in no repetitions
        # and an ease factor of 1.3, with an interval of 0 days.
        card3 = Mock()
        card3.difficulty = 1.0
        card3.repititions = 0
        card3.ease_factor = 1.5
        card3.interval = 0
        card3.next_review = None

        scheduler = Scheduler()
        scheduler.modify_card(card3)
        self.assertEqual(card3.difficulty, 1.0)
        self.assertEqual(card3.repititions, 0)
        self.assertEqual(card3.interval, 1)
        self.assertAlmostEqual(card3.ease_factor, 1.3)

    def test_modify_card_five_difficulty_second_repitition(self):
        card = Mock()
        card.difficulty = 5.0
        card.repititions = 1
        card.ease_factor = 2.0
        card.interval = 1
        card.next_review = None

        scheduler = Scheduler()
        scheduler.modify_card(card)
        self.assertEqual(card.difficulty, 5.0)
        self.assertEqual(card.repititions, 2)
        self.assertEqual(card.interval, 6)
        # Ease factor increases by 0.1
        self.assertAlmostEqual(card.ease_factor, 2.1)

    def test_modify_card_five_difficulty_third_repitition(self):
        card = Mock()
        card.difficulty = 5.0
        card.repititions = 2
        card.ease_factor = 2.0
        card.interval = 6
        card.next_review = None

        scheduler = Scheduler()
        scheduler.modify_card(card)
        self.assertEqual(card.difficulty, 5.0)
        self.assertEqual(card.repititions, 3)
        # Interval = int(6 * 2.0) = 12
        self.assertEqual(card.interval, 12)
        # Ease factor increases by 0.1
        self.assertAlmostEqual(card.ease_factor, 2.1)

    def test_modify_card_two_difficulty_second_repitition(self):
        card = Mock()
        card.difficulty = 2.0
        card.repititions = 1
        card.ease_factor = 1.5
        card.interval = 1
        card.next_review = None

        scheduler = Scheduler()
        scheduler.modify_card(card)
        self.assertEqual(card.difficulty, 2.0)
        self.assertEqual(card.repititions, 0)
        self.assertEqual(card.interval, 1)
        # New EF: 1.5 + (0.1 - (5-2)*(0.08 + (5-2)*0.02))
        # (5-2)=3, 0.08+0.06=0.14, 3*0.14=0.42, 0.1-0.42=-0.32, 1.5-0.32=1.18, but clamped to 1.3
        self.assertAlmostEqual(card.ease_factor, 1.3)

    def test_modify_card_minimum_ease_factor(self):
        card = Mock()
        card.difficulty = 1.0
        card.repititions = 5
        card.ease_factor = 1.3
        card.interval = 10
        card.next_review = None

        scheduler = Scheduler()
        scheduler.modify_card(card)
        # Should stay at 1.3, never decrease
        self.assertAlmostEqual(card.ease_factor, 1.3)

    def test_sort_cards(self):
        # Create mock cards with different next_review and ease_factor values
        card1 = Mock(id=1, next_review=datetime(2023, 10, 1), ease_factor=1.5)
        card2 = Mock(id=2, next_review=datetime(2023, 10, 2), ease_factor=1.2)
        card3 = Mock(id=3, next_review=datetime(2023, 10, 1), ease_factor=1.3)
        card4 = Mock(id=4, next_review=datetime(2023, 10, 3), ease_factor=1.5)

        cards = [card1, card2, card3, card4]
        scheduler = Scheduler()
        sorted_cards = scheduler.sort_cards(cards)
        # Correct expected order
        self.assertEqual(sorted_cards, [card3, card1, card2, card4])
        self.assertEqual(sorted_cards[0].id, 3)
        self.assertEqual(sorted_cards[1].id, 1)
        self.assertEqual(sorted_cards[2].id, 2)
        self.assertEqual(sorted_cards[3].id, 4)

