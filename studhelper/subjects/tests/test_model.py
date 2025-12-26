from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from subjects.models import Subject

class SubjectModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username='tester', password='1234')

    def test_create_subject(self):
        subject = Subject.objects.create(name="Политэкономия", user=self.user)
        self.assertEqual(subject.name, "Политэкономия")
        self.assertEqual(subject.user, self.user)
        self.assertTrue(subject.slug)  # Slug должен быть не пустым

    def test_slug_generated_from_name(self):
        subject = Subject.objects.create(name="История науки", user=self.user)
        self.assertEqual(subject.slug, "istoriia-nauki")

    def test_slug_unique_for_same_names(self):
        s1 = Subject.objects.create(name="Биология", user=self.user)
        s2 = Subject.objects.create(name="Биология", user=self.user)
        self.assertNotEqual(s1.slug, s2.slug)
        self.assertTrue(s2.slug.startswith("biologiia-"))  # biologiia-1 и т.д.

    def test_empty_name_slug_fallback(self):
        subject = Subject.objects.create(name="", user=self.user)
        self.assertTrue(subject.slug.startswith("subject"))

    def test_get_absolute_url(self):
        subject = Subject.objects.create(name="Химия", user=self.user)
        expected_url = reverse('subject_detail', kwargs={'slug': subject.slug})
        self.assertEqual(subject.get_absolute_url(), expected_url)
