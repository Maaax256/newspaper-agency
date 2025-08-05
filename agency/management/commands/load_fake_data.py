from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from agency.models import Newspaper, Topic
from faker import Faker

class Command(BaseCommand):
    help = "Populates the database with fake data for testing and development"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Loading fake data...")
        fake = Faker()

        topics = []
        for _ in range(20):
            topic = Topic.objects.create(name=fake.unique.word())
            topics.append(topic)
            self.stdout.write(f"Created topic: {topic.name}")

        redactors = []
        User = get_user_model()
        for _ in range(20):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.user_name()
            email = fake.email()
            password = fake.password()
            years_of_experience = fake.random_int(min=0, max=50)
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                years_of_experience=years_of_experience,
            )
            redactors.append(user)
            self.stdout.write(f"Created redactor: {user.username} ({password})")

        for _ in range(20):
            title = fake.sentence(nb_words=6)
            content = fake.text(max_nb_chars=1000)

            newspaper = Newspaper.objects.create(
                title=title,
                content=content,
            )
            newspaper.redactors.set(fake.random_elements(
                elements=redactors, length=fake.random_int(min=1, max=7), unique=True
            ))
            newspaper.topics.set(fake.random_elements(
                elements=topics, length=fake.random_int(min=1, max=7), unique=True
            ))
            newspaper.save()
            self.stdout.write(f"Created newspaper: {newspaper.title}")

        self.stdout.write(self.style.SUCCESS("Successfully loaded fake data."))
