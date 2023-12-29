from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Project, EnglishOptional,student_scores
from django.utils import timezone

class StudentScoresModelTestCase(TestCase):
    def setUp(self):
        self.student_score = student_scores.objects.create(
            subject="Math",
            score=85.5
        )

    def test_str_representation(self):
        self.assertEqual(str(self.student_score), "Math - 85.5")

