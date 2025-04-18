from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from agency.models import Newspaper, Topic


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Loading test data...")

        topics = []
        for i in range(1, 21):
            topic = Topic.objects.create(name=f"Topic {i}")
            topics.append(topic)
            self.stdout.write(f"Created topic: {topic}")

        redactors = []
        User = get_user_model()
        for i in range(1, 21):
            first_name = f"first_name{i}"
            last_name = f"last_name{i}"
            username = f"redactor{i}"
            email = f"redactor{i}@example.com"
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=f"password{i}",
                years_of_experience=i
            )
            redactors.append(user)
            self.stdout.write(f"Created redactor: {user}")

        for i in range(1, 21):
            newspaper = Newspaper.objects.create(
                title=f"Newspaper {i}",
                content=f"Content of newspaper {i}. This is a test article. "
                        f"Lorem ipsum dolor sit amet, consectetur adipiscing elit...",
            )
            newspaper.redactors.set(redactors[i % 5: (i % 5 + 3)])
            newspaper.topics.set(topics[i % 5: (i % 5 + 3)])
            newspaper.save()
            self.stdout.write(f"Created newspaper: {newspaper}")

        self.stdout.write(self.style.SUCCESS("Successfully loaded test data."))
