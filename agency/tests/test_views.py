from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from agency.models import Newspaper, Topic

User = get_user_model()

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            years_of_experience=10,
        )
        self.topic = Topic.objects.create(name="Test Topic")
        self.newspaper = Newspaper.objects.create(
            title="Test Newspaper", content="Test Content"
        )
        self.newspaper.redactors.add(self.user)
        self.newspaper.topics.add(self.topic)

    def test_index_view(self):
        """
        Test that the index view returns a 200 status code and
        contains the top experienced redactors.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("agency:home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("top_exp_redactors", response.context)

    def test_newspaper_list_view(self):
        """
        Test that NewspaperListView returns a 200 status code and
        displays all newspapers ordered by title.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("agency:newspaper-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("newspaper_list", response.context)
        self.assertQuerySetEqual(
            response.context["newspaper_list"],
            [self.newspaper],
            ordered=True,
        )

    def test_redactor_list_view(self):
        """
        Test that RedactorListView returns a 200 status code and
        displays all redactors ordered by last name.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("agency:redactor-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("redactor_list", response.context)

    def test_topic_list_view(self):
        """
        Test that TopicListView returns a 200 status code and
        displays all topics ordered by name.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("agency:topic-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("topic_list", response.context)
        self.assertQuerySetEqual(
            response.context["topic_list"], [self.topic], ordered=True
        )

    def test_my_newspapers_list_view(self):
        """
        Test that MyNewspapersListView returns a 200 status code and
        displays the current user's newspapers.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("agency:my-newspapers"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("newspaper_list", response.context)
        self.assertQuerySetEqual(
            response.context["newspaper_list"], [self.newspaper], ordered=True
        )

    def test_newspaper_detail_view(self):
        """
        Test that NewspaperDetailView returns a 200 status code and
        displays the correct newspaper details.
        """
        url = reverse("agency:newspaper-detail", args=[self.newspaper.pk])
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["newspaper"], self.newspaper)

    def test_redactor_detail_view(self):
        """
        Test that RedactorDetailView returns a 200 status code and
        displays the correct redactor details.
        """
        url = reverse("agency:redactor-detail", args=[self.user.pk])
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"], self.user)

    def test_topic_detail_view(self):
        """
        Test that TopicDetailView returns a 200 status code and
        displays the correct topic details.
        """
        url = reverse("agency:topic-detail", args=[self.topic.pk])
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["topic"], self.topic)

    def test_newspaper_create_view(self):
        """
        Test that NewspaperCreateView successfully creates a newspaper.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("agency:newspaper-create"),
            {
                "title": "New Test Newspaper",
                "content": "New Test Content",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Newspaper.objects.count(), 2)

    def test_newspaper_update_view(self):
        """
        Test that NewspaperUpdateView successfully updates a newspaper.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("agency:newspaper-update", args=[self.newspaper.pk]),
            {"title": "Updated Newspaper", "content": "Updated Content"},
        )
        self.assertEqual(response.status_code, 302)
        self.newspaper.refresh_from_db()
        self.assertEqual(self.newspaper.title, "Updated Newspaper")

    def test_newspaper_delete_view(self):
        """
        Test that NewspaperDeleteView successfully deletes a newspaper.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("agency:newspaper-delete", args=[self.newspaper.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Newspaper.objects.count(), 0)

    def test_profile_update_view(self):
        """
        Test that ProfileUpdateView successfully updates a user profile.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("agency:profile-update", args=[self.user.pk]),
            {
                "first_name": "Updated",
                "last_name": "User",
                "years_of_experience": 15,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.years_of_experience, 15)

    def test_registration_view(self):
        """
        Test that RegistrationView successfully registers a user.
        """
        response = self.client.post(
            reverse("agency:redactor-create"),
            {
                "username": "newuser",
                "password1": "qazpassword",
                "password2": "qazpassword",
                "first_name": "New",
                "last_name": "User",
                "email": "new@example.com",
                "years_of_experience": 5,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.filter(username="newuser").count(), 1)
