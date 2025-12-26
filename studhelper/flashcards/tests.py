from django.test import TestCase
from django.contrib.auth import get_user_model
from subjects.models import Subject
from topics.models import Topic
from .models import Flashcard

class FlashcardModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="user", password="pass123")
        self.subject = Subject.objects.create(name="Алгебра", slug="alg", user=self.user)
        self.topic = Topic.objects.create(user=self.user, subject=self.subject, name="Квадратные уравнения")
        self.flashcard = Flashcard.objects.create(
            question="Как вычисляется дискриминант?",
            answer="D = b^2 - 4ac",
            topic=self.topic
        )

    def test_flashcard_belongs_to_topic(self):
        self.assertEqual(self.flashcard.topic, self.topic)

    def test_cascade_delete_topic_deletes_flashcard(self):
        flashcard_pk = self.flashcard.pk
        self.topic.delete()
        # Проверяем, что карточки с этим topic удалились
        self.assertFalse(Flashcard.objects.filter(pk=flashcard_pk).exists())

    def test_cascade_delete_subject_deletes_flashcard(self):
        flashcard_pk = self.flashcard.pk
        self.subject.delete()
        # Удаление subject должно вызвать удаление topic и, соответственно, flashcard
        self.assertFalse(Flashcard.objects.filter(pk=flashcard_pk).exists())

    def test_cascade_delete_user_deletes_flashcard(self):
        flashcard_pk = self.flashcard.pk
        self.user.delete()
        # Удаление user вызывает удаление subject, дальше topic, дальше flashcard
        self.assertFalse(Flashcard.objects.filter(pk=flashcard_pk).exists())