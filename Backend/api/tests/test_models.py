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

