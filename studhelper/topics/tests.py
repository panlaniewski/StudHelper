from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from subjects.models import Subject
from .models import Topic

class TopicModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="user", password="1234")
        self.subject = Subject.objects.create(name="Оптика", slug="optics", user=self.user)

    def test_create_topic_minimal_fields(self):
        topic = Topic.objects.create(
            user=self.user,
            subject=self.subject,
            name="Дифракция"
        )
        self.assertEqual(topic.name, "Дифракция")
        self.assertEqual(topic.user, self.user)
        self.assertEqual(topic.subject, self.subject)
        self.assertFalse(topic.is_archived)
        self.assertIsNotNone(topic.created_at)
        self.assertIsNotNone(topic.updated_at)

    def test_create_topic_with_workbook(self):
        content = "<p>Текст <img src='/media/test_image.png'> и картинка <img src='/media/img2.jpg'></p>"
        topic = Topic.objects.create(
            user=self.user, subject=self.subject, name="Оптика", workbook=content
        )
        images = topic.get_images()
        self.assertIn('/media/test_image.png', images)
        self.assertNotIn('/media/img2.jpg', images)
        self.assertEqual(len(images), 2)

    def test_get_absolute_url(self):
        topic = Topic.objects.create(user=self.user, subject=self.subject, name="Формулы Френеля")
        url = topic.get_absolute_url()
        expected = reverse("topic_detail", kwargs={"slug": self.subject.slug, "pk": topic.pk})
        self.assertEqual(url, expected)

    def test_archive_flag(self):
        topic = Topic.objects.create(user=self.user, subject=self.subject, name="Архив", is_archived=True)
        self.assertTrue(topic.is_archived)

    def test_get_images_empty(self):
        topic = Topic.objects.create(user=self.user, subject=self.subject, name="Без картинок", workbook="")
        self.assertEqual(topic.get_images(), [])
        topic2 = Topic.objects.create(user=self.user, subject=self.subject, name="Workbook None", workbook=None)
        self.assertEqual(topic2.get_images(), [])

    def test_ordering_meta(self):
        # Проверяем, что сортировка работает: сначала по order, потом по name
        t1 = Topic.objects.create(user=self.user, subject=self.subject, name="B", order=1)
        t2 = Topic.objects.create(user=self.user, subject=self.subject, name="A", order=1)
        t3 = Topic.objects.create(user=self.user, subject=self.subject, name="C", order=2)
        topics = list(Topic.objects.all())
        self.assertEqual([t.name for t in topics], ["A", "B", "C"])

class ModelRelationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='student', password='pass')
        self.subject = Subject.objects.create(name="Python", user=self.user)
        self.topic = Topic.objects.create(name="классы", subject=self.subject, user=self.user)

    def test_topic_subject_relation(self):
        # Topic связан с Subject
        self.assertEqual(self.topic.subject, self.subject)
        # Subject связан с Topic через topic_set
        self.assertIn(self.topic, self.subject.topic_set.all())

    def test_topic_user_relation(self):
        # Topic связан с User напрямую (related_name="topics")
        self.assertEqual(self.topic.user, self.user)
        # User имеет topics через related_name
        self.assertIn(self.topic, self.user.topics.all())

    def test_cascade_delete_user_deletes_subject_and_topic(self):
        # Удаляем пользователя, должны удалиться и Subject, и Topic
        self.user.delete()
        self.assertFalse(Subject.objects.exists())
        self.assertFalse(Topic.objects.exists())

    def test_cascade_delete_subject_deletes_topic(self):
        topic_pk = self.topic.pk
        subject_pk = self.subject.pk
        self.subject.delete()
        self.assertFalse(Topic.objects.filter(pk=topic_pk).exists())
        self.assertFalse(Topic.objects.filter(subject_id=subject_pk).exists())
