from django.test import TestCase
from unittest.mock import Mock
from quiz.services.scheduler import Scheduler
from quiz.models import Deck, FlashCard

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