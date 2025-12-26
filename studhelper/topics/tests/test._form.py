from django.test import TestCase
from django.contrib.auth import get_user_model
from topics.models import Topic
from topics.form import TopicForm
from subjects.models import Subject

class TopicFormValidationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="user1", password="123")
        self.other_user = get_user_model().objects.create_user(username="user2", password="321")
        # Допустим, на одну тему нужен связанный предмет (subject)
        self.subject = Subject.objects.create(name="Биология", slug="biology", user=self.user)
        # Уже есть тема с таким именем для self.user
        self.topic = Topic.objects.create(name="Генетика", subject=self.subject, user=self.user)

    def test_clean_name_duplicate_for_user(self):
        form = TopicForm(data={"name": "Генетика"}, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("Тема с таким именем уже существует!", form.errors['name'])

    def test_clean_name_ok_for_another_user(self):
        form = TopicForm(data={"name": "Генетика"}, user=self.other_user)
        self.assertTrue(form.is_valid())

    def test_clean_name_valid_if_not_exists(self):
        form = TopicForm(data={"name": "Биосинтез"}, user=self.user)
        self.assertTrue(form.is_valid())

    def test_clean_name_empty(self):
        form = TopicForm(data={"name": ""}, user=self.user)
        self.assertFalse(form.is_valid())
        # Обычно стандартная валидация формы сработает, а не кастомная!
        self.assertIn("Обязательное поле", str(form.errors['name']))