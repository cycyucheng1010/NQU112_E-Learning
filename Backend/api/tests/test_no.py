from django.test import TestCase
from api.models import Project
from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Project, EnglishOptional,student_scores
from django.utils import timezone


class EnglishOptionalCreateTestCase(TestCase):
    def setUp(self):
        EnglishOptional.objects.create(
            topic_number="1",
            answer_A="Option A",
            answer_B="Option B",
            answer_C="Option C",
            answer_D="Option D",
            answer="A",
            year=2023
        )

    def test_get_english_optional(self):
        english_optional = EnglishOptional.objects.get(topic_number="1")
        self.assertEqual(english_optional.topic_number, "1")
        self.assertEqual(english_optional.answer_A, "Option A")
        self.assertEqual(english_optional.answer_B, "Option B")
        self.assertEqual(english_optional.answer_C, "Option C")
        self.assertEqual(english_optional.answer_D, "Option D")
        self.assertEqual(english_optional.answer, "A")
        self.assertEqual(english_optional.year, 2023)
    
    def test_no(self):

        print("no test")
