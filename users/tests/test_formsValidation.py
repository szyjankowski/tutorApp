from django.test import TestCase
from users.forms import CustomUserCreationForm


class CustomUserCreationFormTest(TestCase):
    def test_form_has_fields(self):
        form = CustomUserCreationForm()
        expected_fields = {"email", "password1", "password2"}
        self.assertEqual(set(form.fields), expected_fields)

    def test_form_validation_for_blank_items(self):
        form = CustomUserCreationForm(
            data={"email": "", "password1": "password123", "password2": "password123"}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["This field is required."])
