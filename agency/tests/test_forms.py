from django.test import TestCase
from django.contrib.auth import get_user_model
from agency.forms import NewspaperForm, RedactorCreationForm, RedactorUpdateForm
from agency.models import Topic

User = get_user_model()

class FormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
            email="test@example.com"
        )
        self.topic = Topic.objects.create(name="Test Topic")

    def test_newspaper_form_valid_data(self):
        """
        Test that NewspaperForm is valid with correct data.
        """
        form_data = {
            "title": "Test Newspaper",
            "content": "Test Content",
        }
        form = NewspaperForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_newspaper_form_redactors_and_topics(self):
        """
        Test that NewspaperForm handles redactors and topics correctly.
        """
        form_data = {
            "title": "Test Newspaper",
            "content": "Test Content",
            "redactors": [self.user.id],
            "topics": [self.topic.id],
        }
        form = NewspaperForm(data=form_data)
        self.assertTrue(form.is_valid())
        newspaper = form.save()
        newspaper.redactors.add(self.user)
        newspaper.topics.add(self.topic)
        self.assertEqual(newspaper.redactors.count(), 1)
        self.assertEqual(newspaper.topics.count(), 1)

    def test_redactor_creation_form_valid_data(self):
        """
        Test that RedactorCreationForm is valid with correct data.
        """
        form_data = {
            "username": "newuser",
            "password2": "qazpassword",
            "password1": "qazpassword",
            "first_name": "New",
            "last_name": "User",
            "email": "new@example.com",
            "years_of_experience": 5,
        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_redactor_creation_form_invalid_years(self):
        """
        Test that RedactorCreationForm is invalid with invalid years_of_experience.
        """
        form_data = {
            "username": "newuser",
            "password": "newpassword",
            "first_name": "New",
            "last_name": "User",
            "email": "new@example.com",
            "years_of_experience": -1,
        }
        form = RedactorCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)

        form_data["years_of_experience"] = 61
        form = RedactorCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)

    def test_redactor_update_form_valid_data(self):
        """
        Test that RedactorUpdateForm is valid with correct data.
        """
        form_data = {
            "first_name": "Updated",
            "last_name": "User",
            "years_of_experience": 10,
        }
        form = RedactorUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_redactor_update_form_invalid_years(self):
        """
        Test that RedactorUpdateForm is invalid with invalid years_of_experience.
        """
        form_data = {
            "first_name": "Updated",
            "last_name": "User",
            "years_of_experience": -5,
        }
        form = RedactorUpdateForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)

        form_data["years_of_experience"] = 65
        form = RedactorUpdateForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)

