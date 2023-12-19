from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Project, EnglishOptional,student_scores
from django.utils import timezone

class ProjectModelTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Test Project",
            start_date=timezone.now(),
            end_date=timezone.now(),
            comments="Test comments",
            status="In Progress"
        )

    def test_str_representation(self):
        self.assertEqual(str(self.project), "Test Project")

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

class StudentScoresModelTestCase(TestCase):
    def setUp(self):
        self.student_score = student_scores.objects.create(
            subject="Math",
            score=85.5
        )

    def test_str_representation(self):
        self.assertEqual(str(self.student_score), "Math - 85.5")

