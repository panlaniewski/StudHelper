from django.test import TestCase
from django.contrib.auth import get_user_model
from subjects.models import Subject
from subjects.forms import SubjectForm

class SubjectFormValidationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="u1", password="pass")
        self.other_user = get_user_model().objects.create_user(username="u2", password="pass")
        self.subject = Subject.objects.create(name="Русский", user=self.user)

    def test_clean_name_returns_error_if_duplicate_for_user(self):
        form = SubjectForm(data={'name': 'Русский'}, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("Предмет с таким именем уже существует!", form.errors['name'])

    def test_clean_name_ok_for_another_user(self):
        form = SubjectForm(data={'name': 'Русский'}, user=self.other_user)
        self.assertTrue(form.is_valid())

    def test_clean_name_ok_if_subject_not_exists(self):
        form = SubjectForm(data={'name': 'Математика'}, user=self.user)
        self.assertTrue(form.is_valid())

    def test_clean_name_ok_for_empty(self):
        # Чисто пустое — не сработает уникальный валидатор (но проверит required=True самой формы)
        form = SubjectForm(data={'name': ''}, user=self.user)
        self.assertFalse(form.is_valid())

class SubjectUpdateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="user1", password="password")
        self.other_user = get_user_model().objects.create_user(username="user2", password="123456")
        self.subj1 = Subject.objects.create(name="Математика", user=self.user)
        self.subj2 = Subject.objects.create(name="Русский", user=self.user)
        self.subj_other = Subject.objects.create(name="Теория вероятностей", user=self.other_user)

    def test_update_subject_to_unique_name(self):
        form = SubjectForm(data={"name": "Биология"}, user=self.user, instance=self.subj1)
        self.assertTrue(form.is_valid())
        # Сохраняем изменения
        updated = form.save()
        self.assertEqual(updated.name, "Биология")

    def test_update_subject_to_duplicate_name_fail(self):
        # Пытаемся subj1 (Математика) изменить на имя subj2 (Русский) у того же пользователя
        form = SubjectForm(data={"name": "Русский"}, user=self.user, instance=self.subj1)
        self.assertFalse(form.is_valid())
        self.assertIn("Предмет с таким именем уже существует!", form.errors['name'])

    def test_update_subject_to_same_name_ok(self):
        # Изменяем на то же самое имя — должно быть ок
        form = SubjectForm(data={"name": "Математика"}, user=self.user, instance=self.subj1)
        self.assertTrue(form.is_valid())
        updated = form.save()
        self.assertEqual(updated.name, "Математика")

    def test_update_subject_to_duplicate_name_from_another_user(self):
        # Можно изменить имя на такое же, если оно есть только у другого пользователя
        form = SubjectForm(data={"name": "Теория вероятностей"}, user=self.user, instance=self.subj2)
        self.assertTrue(form.is_valid())
        updated = form.save()
        self.assertEqual(updated.name, "Теория вероятностей")